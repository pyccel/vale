function f(x, y) 
  setmetatable(_ENV, { __index=math })  
  local ky = 2.0
  local kx = 2.0
  return ((kx * pi) * (kx * pi) * (kx * pi) * (kx * pi) + (ky * pi) * (ky * pi) * (ky * pi) * (ky * pi))  * sin(kx * pi * x) * sin(ky * pi * y) 
end 
