A = dir('*.csv');
tableArray = cell(length(A),1);

for i = 1:length(A)
    currentTable = readtable(A(i).name);
    tableArray{i} = currentTable;
    rateLen = length(currentTable{:,2})-1;

    radioName = A(i).name(14:19);
    radioDate = A(i).date(1:11);

    % Convert timestamp column (assumed in HH:MM:SS format) to datetime
    
    timestamps = datetime(string(currentTable{2:rateLen,2}), 'InputFormat', 'HH:mm:ss');

    % Detect if timestamps reset after midnight
    time_diffs = seconds(diff(timestamps)); 
    midnight_jumps = find(time_diffs < 0); % Negative difference means the time reset

    % Create a continuous time axis
    elapsed_time = seconds(timestamps - timestamps(1)); % Start from 0 seconds
    for j = 1:length(midnight_jumps)
        elapsed_time(midnight_jumps(j)+1:end) = ...
            elapsed_time(midnight_jumps(j)+1:end) + 24*3600; % Add 24 hours in seconds
    end

    % Compute packet rate
    data1 = diff(cellfun(@(x) str2double(regexprep(x, '[^\d]', '')),currentTable{1:rateLen,26}))./5;
    data2 = diff(cellfun(@(x) str2double(regexprep(x, '[^\d]', '')),currentTable{1:rateLen,28}))./5;

    % Filter out anomalies
    filtered_data1 = data1(data1 <= 50 & data1 >= 0);
    filtered_data2 = data2(data2 <= 50 & data2 >= 0);
    mean1 = mean(filtered_data1);
    mean2 = mean(filtered_data2);

    % Plot using continuous elapsed time
    figure
    plot(elapsed_time(1:end), data1, 'b-', 'DisplayName', 'Base Station Packets Sent');
    hold on
    plot(elapsed_time(1:end), data2, 'r-', 'DisplayName', 'Receiver Packets Received');

    % Add Mean Lines (without appearing in legend)
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
    title(sprintf('%s %s', radioName, radioDate));
    legend('show');
    ylim([0 30]);
    grid on;
end
