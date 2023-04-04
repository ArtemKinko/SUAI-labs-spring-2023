global l15 l25 l95 l05 l53 l57 l64 l68 l16 l26 l96 l06 l56 l65;

l15 = 0.3; 
l25 = 0.1; 
l95 = 0.5; 
l05 = 0.8;

l53 = 0.2; 
l57 = 0.1; 
l56 = 0.5;

l64 = 0.2; 
l68 = 0.1;
l65 = 0.5;
 
l16 = 0.7;
l26 = 0.9;
l96 = 0.5;
l06 = 0.2;

initial = [0; 0; 0; 0; 0.3; 0.7; 0; 0; 0; 0];


time = [0, 25];

[T, Y] = ode45('LotVol', time, initial); 

for i = 1:10
  plot(Y(:,i)); hold on
end

