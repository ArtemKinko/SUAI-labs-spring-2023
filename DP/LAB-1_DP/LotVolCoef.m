function result = LotVolCoef( lambda )
 
 s = size(lambda);
 if (s(1) ~= s(2))
     result = 0;
     return;
 end
 s = s(1);
 
 d = zeros(s); 
 
 for k = 1:s
     for i = 1:s
         d(k, i) = lambda(i, k);
     end
 end 
 
 for k = 1:s
     for i = 1:s
         d(k, k) = d(k, k) - lambda(k, i);
     end
 end
  
 result = d;
end
