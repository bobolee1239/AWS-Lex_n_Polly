% matEnd.m for TCP Communication
clear all; clc;

server_name = 'localhost';
portNum = 10000;

t = tcpip(server_name, portNum);
fprintf("connecting to %s portNum %s\n", server_name, portNum);
t.InputBufferSize = 32;

fopen(t);

msg = 'This is the message. It will be repeated.';
fprintf('sending "%s" ...\n', msg);
fprintf(t, msg);

% look for response
amount_received = 0;
amount_expected = strlength(msg);

while amount_received < amount_expected
    data = fscanf(t, '%c', 16);
    amount_received = amount_received + strlength(data);
    fprintf("received %s\n", data)
end

fclose(t);
delete(t);
clear t;