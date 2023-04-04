function result = LotVolCoefSource()
%LOTVOLCOEFSOURCE Summary of this function goes here
%   Detailed explanation goes here
 global l15 l25 l95 l05 l53 l57 l64 l68 l16 l26 l96 l06 l56 l65;
 
 lambda = [
% --1 --2 --3 --4 --5 --6 --7 --8 --9 -10
    0   0   0   0 l15 l16   0   0   0   0;
    0   0   0   0 l25 l26   0   0   0   0;
    1   0   0   0   0   0   0   0   0   0;
    0   1   0   0   0   0   0   0   0   0;
    0   0 l53   0   0 l56 l57   0   0   0;
    0   0   0 l64 l65   0   0 l68   0   0;
    0   0   0   0   0   0   0   0   1   0;
    0   0   0   0   0   0   0   0   0   1;
    0   0   0   0 l95 l96   0   0   0   0;
    0   0   0   0 l05 l06   0   0   0   0
% --1 --2 --3 --4 --5 --6 --7 --8 --9 -10
 ];
 result = LotVolCoef(lambda);
 
end

