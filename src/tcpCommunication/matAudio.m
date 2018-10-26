%% ---------------- Send audio -------------------
close all; clear all; clc;
% connect to tcp/ip server
server_ip = 'localhost';
portNum = 10000;

% create tcp/ip obj 
t = tcpi p(server_ip, portNum);
t.OutputBufferSize = 512;
t.ByteOrder = 'littleEndian';
fprintf('Connecting to server ...\n')
fopen(t);

%%


flushoutput(t);
flushinput(t);

REQUEST1 = 'Request.m4a';
REQUEST2 = 'yes.m4a';
[requestAudio, fs] = audioread(REQUEST2);

% Transform double 2 signed int16 as byte;
%   * 1. represent as int 
%   * 2. little-endian order
%   * 3. sampling rate 8k Hz
requestAudio = resample(requestAudio, 8000, fs);

requestAudio = requestAudio ./ max(requestAudio);
requestAudio = cast(requestAudio .* (2^15), 'int16');


numPush = floor(length(requestAudio)/t.OutputBufferSize*2) + 1;



if strcmp(t.Status, 'open')
    fprintf('Sending data ...\n')
    % transport data
    for i=1:1:numPush
        if i == numPush
            fwrite(t, requestAudio((i-1)*256+1:end, 1), 'int16');
        else
            fwrite(t, requestAudio((i-1)*256+1:i*256, 1), 'int16');
        end
    end
else
    fprintf('Connection failed!\n')
end

%% 
fclose(t);