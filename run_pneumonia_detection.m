% Pneumonia Detection from Chest X-rays
% This script loads your dataset and performs pneumonia detection

%% Clear workspace
clear; close all; clc;

%% Set up paths (update these to match your folder structure)
projectDir = 'd:\\CascadeProjects\\medical_imaging_analysis';
dataDir = fullfile(projectDir, 'data');

% Check if data directory exists
if ~isfolder(dataDir)
    error('Data directory not found at: %s', dataDir);
end

%% Load and explore the dataset
% Create image datastore
imds = imageDatastore(fullfile(dataDir, 'dataset'), ...
    'IncludeSubfolders', true, ...
    'LabelSource', 'foldernames');

% Display class names and counts
[classNames, counts] = countEachLabel(imds);
disp('Dataset Summary:');
disp(classNames);

% Display some sample images
figure('Name', 'Sample Images from Dataset');
numImages = min(4, numel(imds.Files));
perm = randperm(numel(imds.Files), numImages);
for i = 1:numImages
    subplot(2, 2, i);
    img = readimage(imds, perm(i));
    imshow(img);
    title(char(imds.Labels(perm(i))));
end

%% Preprocess images
% Resize images to 224x224 for ResNet-50
inputSize = [224 224];
imds.ReadFcn = @(loc)imresize(imread(loc), inputSize);

% Split into training and validation sets
[imdsTrain, imdsVal] = splitEachLabel(imds, 0.7, 'randomized');

%% Load pre-trained ResNet-50
net = resnet50;

% Display network architecture
analyzeNetwork(net);

%% Modify network for binary classification
lgraph = layerGraph(net);
numClasses = 2;

% Replace the last few layers for transfer learning
newFCLayer = fullyConnectedLayer(numClasses, ...
    'Name', 'New_FC', ...
    'WeightLearnRateFactor', 10, ...
    'BiasLearnRateFactor', 10);

newClassLayer = classificationLayer('Name', 'New_Classification');

lgraph = replaceLayer(lgraph, 'fc1000', newFCLayer);
lgraph = replaceLayer(lgraph, 'ClassificationLayer_fc1000', newClassLayer);

%% Training options
options = trainingOptions('adam', ...
    'MiniBatchSize', 32, ...
    'MaxEpochs', 5, ...
    'InitialLearnRate', 1e-4, ...
    'Shuffle', 'every-epoch', ...
    'ValidationData', imdsVal, ...
    'ValidationFrequency', 30, ...
    'Verbose', true, ...
    'Plots', 'training-progress');

%% Train the network
[net, info] = trainNetwork(imdsTrain, lgraph, options);

%% Save the trained model
save(fullfile(projectDir, 'pneumonia_model.mat'), 'net');

disp('Training complete! Model saved as pneumonia_model.mat');

%% Test the model on a single image
% Uncomment and modify this section to test on new images
% testImage = fullfile(dataDir, 'test_image.jpg');
% if isfile(testImage)
%     img = imread(testImage);
%     img = imresize(img, inputSize);
%     [label, score] = classify(net, img);
%     figure;
%     imshow(img);
%     title(sprintf('Prediction: %s (%.2f%%)', char(label), max(score)*100));
% end
