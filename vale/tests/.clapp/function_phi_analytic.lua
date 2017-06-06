function phi_analytic(x, y) 
  setmetatable(_ENV, { __index=math })  
  local ky = 2.0
  local kx = 2.0
  return sin(kx * pi * x) * sin(ky * pi * y) 
end 
