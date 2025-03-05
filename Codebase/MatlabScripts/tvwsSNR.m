A = dir('*.csv');
tableArray = cell(length(A),1);
%figure
for i = 1:length(A)
    currentTable = readtable(A(i).name);
    tableArray{i} = currentTable;
    rateLen = length(currentTable{:,2})-1;
    %packet_numbers = cellfun(@(x) str2double(regexprep(x, '[^\d]', '')), packet_data);

    radioName = A(i).name(14:19);
    radioDate = A(i).date(1:11);

    figure
    %plot(currentTable{:,2}, currentTable{:,26}, '*-');
    %data1 = diff(cellfun(@(x) str2double(regexprep(x, '[^\d]', '')),currentTable{1:rateLen,26}));
    %data2 = diff(cellfun(@(x) str2double(regexprep(x, '[^\d]', '')),currentTable{1:rateLen,28}));
    %Filter out anamolous spikes in data values
    %filtered_data1 = data1(data1 <= 80);
    %filtered_data2 = data2(data2 <= 80);

    %Divide by 5 to get packet/sec since we polled every 5 seconds
    %filtered_data1 = filtered_data1./5;
    %filtered_data2 = filtered_data2./5;
    %Extract the mean
    %mean1 = mean(filtered_data1);
    %mean2 = mean(filtered_data2);

    
    plot(currentTable{:,2}, currentTable{:,14});
    %plot(currentTable{2:rateLen,2}, diff(cellfun(@(x) str2double(regexprep(x, '[^\d]', '')),currentTable{1:rateLen,26}))./5);
    hold on
    %plot(currentTable{2:rateLen,2}, diff(cellfun(@(x) str2double(regexprep(x, '[^\d]', '')),currentTable{1:rateLen,28}))./5);
    plot(currentTable{:,2}, currentTable{:,24});
    
    legend('Base Station', 'Receiver');
    %hold on
    %yline(mean(filtered_data1), 'k--', 'LineWidth', 2, 'HandleVisibility', 'off');
    %text(1, mean1, sprintf('Mean: %.2f', mean1), 'FontSize', 12, 'FontWeight', 'bold', 'Color', 'k');
    %hold on

    %yline(mean(filtered_data2), 'k--', 'LineWidth', 2, 'HandleVisibility', 'off');
    %text(1, mean2, sprintf('Mean: %.2f', mean2));

    %x_limits = xlim;
    %x_pos = x_limits(1) + (x_limits(2) - x_limits(1)) * 0.05; % Position near left

    % Display mean value text at adjusted position
    %text(x_pos, mean1 + 1, sprintf('Mean: %.2f', mean1), 'FontSize', 12, 'FontWeight', 'bold', 'Color', 'k');
    %text(x_pos, mean2 + 1, sprintf('Mean: %.2f', mean2), 'FontSize', 12, 'FontWeight', 'bold', 'Color', 'k');

    xlabel(['Time']);
    ylabel(['SNR']);
    %title(sprintf('%d MHz | %.1f dBm Tx | %.1f dB Rx Gain',currentTable{1,4}, currentTable{1,6}, currentTable{1,7}));
    title(sprintf('%s %s', radioName, radioDate)); % Set title dynamically

    %title([int2str(currentTable{1,4}), 'MHz | ', currentTable{1,5},'dBm Tx | ', currentTable{1,6},'dB Rx Gain']);
    %ylim([35 45]);
    %break
    %hold on
end

