function result = LotVol(t, y) % первая функция
  coef = LotVolCoefSource();
  [r, c] = size(coef);
  result = zeros(r, 1);
  for i = 1:r
      for j = 1:c
          result(i) = result(i) + coef(i, j) * y(j);
      end
  end
end
