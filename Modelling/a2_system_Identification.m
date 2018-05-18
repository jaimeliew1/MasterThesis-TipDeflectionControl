% Load data files
close all

directory = 'Data/';
files = dir('Data/pitchstep_*.mat');
N = length(files);
filenames = {};
x = {};
y = {};

for i=1:N
    filenames{i} = [directory files(i).name];
    temp = load(filenames{i});
    x{i} = -temp.x; % IF THERE IS A SIGN ERROR, THIS MIGHT CAUSE IT.
    y{i} = temp.y;
end

%% save time series for each wind speed
for i=1:N
    Data{i} = iddata(y{i}', x{i}', 0.01);
end

%% Produce bode plots of input/output pairs and saves to file

for i=1:N
    G{i} = spafdr(Data{i}, [], {0.2, 8*pi});
    %G{i} = spa(Data{i})
    G{i}.Name = filenames{i};

    g = reshape(G{i}.ResponseData, [], 1);
    om = G{i}.Frequency;

    save([directory sprintf('FreqRespFunc_%d.mat', i*2+2)], 'g', 'om')


end


%% plot bode plots

figure; hold on;
bodeSettings = bodeoptions;
bodeSettings.FreqUnits = 'Hz';
%bodeSettings.FreqScale = 'linear';
for i =1:N
    bode(G{i}, bodeSettings)

end

%% Find best fitting number of zeros and poles for each wind speed
np_max = 4;

for i=1:N

    sys = tfest(G{i}, 4, 3); % changed to 3 zeros, not 4. steeper rolloff
    fit = sys.Report.Fit.FitPercent
    figure; hold on;
    bode(G{i}, bodeSettings)
    bode(sys, bodeSettings)
    %xlim([0, 4])
    b = sys.Numerator;
    a = sys.Denominator;
    save([directory sprintf('TransferFunc_%d.mat', i*2+2)], 'b', 'a')

end

