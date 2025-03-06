function data = import_csv_files()
    % Get the script's directory and set base data directory
    scriptDir = fileparts(mfilename('fullpath'));
    rootDir = fullfile(scriptDir, '..', '..');
    baseDir = fullfile(rootDir, 'Data');

    fprintf('Looking in base directory: %s\n', baseDir);

    % Verify if the directory exists
    if ~isfolder(baseDir)
        error('Error: Directory %s does not exist.', baseDir);
    end

    % Get list of date folders
    allFolders = dir(baseDir);
    allFolders = allFolders([allFolders.isdir]);
    allFolderNames = {allFolders.name};

    fprintf('Found %d total folders:\n', length(allFolderNames));
    disp(allFolderNames);

    allFolderNames = setdiff(allFolderNames, {'.', '..'});

    % Filter date folders (MM-DD-YYYY)
    datePattern = '^\d{2}-\d{2}-\d{4}$';
    validDateFolders = allFolderNames(cellfun(@(x) ~isempty(regexp(x, datePattern, 'once')), allFolderNames));

    if isempty(validDateFolders)
        fprintf('No valid date folders found in %s.\n', baseDir);
        return;
    else
        fprintf('Valid date folders found: %s\n', strjoin(validDateFolders, ', '));
    end

    % Initialize data structure
    data.tables = struct();
    data.elapsed_time = struct();
    data.radioNames = struct();
    data.radioDates = struct();

    % Iterate over valid date folders
    for i = 1:length(validDateFolders)
        dateFolderPath = fullfile(baseDir, validDateFolders{i});
        fprintf('Checking folder: %s\n', dateFolderPath);

        % Get list of CSV files in the date folder
        csvFiles = dir(fullfile(dateFolderPath, '*.csv'));
        fprintf('Found %d CSV files in %s\n', length(csvFiles), dateFolderPath);

        if isempty(csvFiles)
            continue;
        end

        for j = 1:length(csvFiles)
            fileName = csvFiles(j).name;
            filePath = fullfile(dateFolderPath, fileName);
            fprintf('Reading file: %s\n', filePath);

            try
                % Detect CSV import options
                opts = detectImportOptions(filePath, 'VariableNamingRule', 'preserve');
                if contains(fileName, 'TVWSScenario')
                    opts.DataLines = 3; % Skip first two lines for TVWSScenario
                end
                currentTable = readtable(filePath, opts);

                % Normalize column names: remove spaces, special chars
                currentTable.Properties.VariableNames = matlab.lang.makeValidName(currentTable.Properties.VariableNames);

                fprintf('Normalized Columns in %s:\n', fileName);
                disp(currentTable.Properties.VariableNames);

                % Extract radio number if applicable
                radioID = "General";
                if contains(fileName, 'TVWSScenario')
                    radioMatch = regexp(fileName, 'radio(\d+)', 'tokens');
                    if ~isempty(radioMatch)
                        radioID = strcat("Radio", radioMatch{1}{1});
                    end
                end

                % Detect timestamp column dynamically
                timestampColumn = [];
                if contains(fileName, 'SoilData')
                    timestampColumn = find(strcmp(currentTable.Properties.VariableNames, 'Timestamp'), 1);
                elseif contains(fileName, 'TVWSScenario')
                    dateCol = find(contains(currentTable.Properties.VariableNames, 'Date_Mon_Day_Year'), 1);
                    timeCol = find(contains(currentTable.Properties.VariableNames, 'Time_Hour_Min_Sec'), 1);
                    if ~isempty(dateCol) && ~isempty(timeCol)
                        timestamps = datetime(strcat(currentTable{:, dateCol}, " ", currentTable{:, timeCol}), ...
                            'InputFormat', 'yyyy-MM-dd HH:mm:ss');
                        timestampColumn = -1;
                    end
                end

                if isempty(timestampColumn)
                    warning('No valid timestamp column found in %s. Skipping...', fileName);
                    data.elapsed_time.(radioID){end+1} = [];
                else
                    try
                        if timestampColumn == -1
                            elapsed_time = seconds(timestamps - timestamps(1));
                        else
                            fprintf('First few timestamps in %s:\n', fileName);
                            disp(currentTable.Timestamp(1:min(5, height(currentTable))));

                            % Convert timestamps for SoilData
                            timestamps = datetime(string(currentTable{:, timestampColumn}), ...
                                'InputFormat', 'HH:mm:ss', 'Format', 'HH:mm:ss');
                            elapsed_time = seconds(timestamps - timestamps(1));
                        end
                        time_diffs = seconds(diff(timestamps));
                        midnight_jumps = find(time_diffs < 0);
                        for k = 1:length(midnight_jumps)
                            elapsed_time(midnight_jumps(k)+1:end) = elapsed_time(midnight_jumps(k)+1:end) + 24*3600;
                        end
                        data.elapsed_time.(radioID){end+1} = elapsed_time;
                    catch
                        warning('Error processing timestamps for file: %s. Skipping...', fileName);
                        data.elapsed_time.(radioID){end+1} = [];
                    end
                end

                % Store table and metadata in struct by radio ID
                if ~isfield(data.tables, radioID)
                    data.tables.(radioID) = {};
                    data.radioNames.(radioID) = {};
                    data.radioDates.(radioID) = {};
                end
                data.tables.(radioID){end+1} = currentTable;
                data.radioNames.(radioID){end+1} = radioID;
                data.radioDates.(radioID){end+1} = validDateFolders{i};
            catch
                warning('Could not read file: %s. Skipping...', fileName);
                fprintf('Checking file content:\n');
                type(filePath); % Print raw file content for debugging
                continue;
            end
        end
    end

    if isempty(fieldnames(data.tables))
        disp('No CSV files found.');
    else
        disp(['Loaded data for ', num2str(length(fieldnames(data.tables))), ' radio instances.']);
    end
end
