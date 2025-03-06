data = import_csv_files();

if isempty(fieldnames(data.tables))
    disp('No data loaded.');
else
    % Loop through each radio category
    radioFields = fieldnames(data.tables); % Get all radio IDs (e.g., Radio1, Radio2)
    
    for r = 1:length(radioFields)
        radioID = radioFields{r}; % Extract radio name
        fprintf('Processing data for %s...\n', radioID);

        for i = 1:length(data.tables.(radioID))
            currentTable = data.tables.(radioID){i};
            
            % Check if elapsed_time exists for this entry
            if i > length(data.elapsed_time.(radioID)) || isempty(data.elapsed_time.(radioID){i})
                warning('Skipping entry %d of %s: No valid elapsed_time data.', i, radioID);
                continue;
            end
            
            elapsed_time = data.elapsed_time.(radioID){i};
            radioName = data.radioNames.(radioID){i};
            radioDate = data.radioDates.(radioID){i};

            % Ensure enough columns exist in the table
            if size(currentTable, 2) < 28
                warning('Skipping file %s due to insufficient columns.', radioName);
                continue;
            end

            % Compute packet rate
            try
                data1 = diff(cellfun(@(x) str2double(regexprep(x, '[^\d]', '')), currentTable{1:end-1, 26}))./5;
                data2 = diff(cellfun(@(x) str2double(regexprep(x, '[^\d]', '')), currentTable{1:end-1, 28}))./5;

                % Filter out anomalies
                filtered_data1 = data1(data1 <= 50 & data1 >= 0);
                filtered_data2 = data2(data2 <= 50 & data2 >= 0);
                mean1 = mean(filtered_data1);
                mean2 = mean(filtered_data2);

                % Plot using continuous elapsed time
                figure
                plot(elapsed_time, data1, 'b-', 'DisplayName', 'Base Station Packets Sent');
                hold on
                plot(elapsed_time, data2, 'r-', 'DisplayName', 'Receiver Packets Received');

                % Add Mean Lines
                yline(mean1, 'k--', 'LineWidth', 2, 'HandleVisibility', 'off');
                yline(mean2, 'k--', 'LineWidth', 2, 'HandleVisibility', 'off');

                % Display Mean Value Text
                x_limits = xlim;
                x_pos = x_limits(1) + (x_limits(2) - x_limits(1)) * 0.05;
                text(x_pos, mean1 + 1, sprintf('Mean: %.2f', mean1), 'FontSize', 12, 'FontWeight', 'bold', 'Color', 'k');
                text(x_pos, mean2 + 1, sprintf('Mean: %.2f', mean2), 'FontSize', 12, 'FontWeight', 'bold', 'Color', 'k');

                % Labels and Title
                xlabel('Elapsed Time (Seconds)');
                ylabel('Packets Per Second');
                title(sprintf('%s - %s', radioName, radioDate));
                legend('show');
                ylim([0 30]);
                grid on;
            catch
                warning('Error processing file for %s. Skipping...', radioName);
            end
        end
    end
end
