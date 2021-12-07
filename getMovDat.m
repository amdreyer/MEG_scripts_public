function [ time, gValue, velocity, q1, q2, q3, q4, q5, q6 ] = getMovDat( posFile, average, returnQ )
%GETMOVDAT
% reads data from Elekta Maxfilter .pos Output file
%
% posFile is a string with full file path
% optional input:
% average - return average values only (default = false)
% returnQ - return quaternions (default = false)
%
% output:
% time - time vector
% gValue - goodness of fit
% velocity - movement velocity in m/s
% q1...6 - quaternions (currently not returned
% err - fit error of HPI coils in m
if nargin<2
    average = false;
    returnQ = false;
elseif nargin <3
    returnQ = false;
end

% read file
file = fopen(posFile);
% get header, rest is float
header = strsplit(fgetl(file));
formatspec = '%f %f %f %f %f %f %f %f %f %f';
% get data
dat = textscan(file,formatspec);
time = dat{1};
gValue = dat{8}; % goodness of fit
% err = dat{9}; % fitting error in m
velocity = dat{10};
if average
    gValue = mean(gValue);
    velocity = mean(velocity);
end;
if returnQ
    q1 = dat{2};
    q2 = dat{3};
    q3 = dat{4};
    q4 = dat{5};
    q5 = dat{6};
    q6 = dat{7};
end;

fclose(file);
end

