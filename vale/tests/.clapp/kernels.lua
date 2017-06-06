
function kernel_b(arr_jacobian, arr_Ni1_0, arr_Ni1_s, arr_Ni2_0, arr_Ni2_s, arr_wvol, arr_x, arr_y, n1, n2, n_rows)
setmetatable(_ENV, { __index=math })  
function_f = require 'function_f' 
setmetatable(_ENV, { __index=function_f }) 


local n1 = math.floor(n1)
local n2 = math.floor(n2)
local n_rows = math.floor(n_rows)
local contribution = 0.0
for g1 = 1, n1 do
for g2 = 1, n2 do
local g = g2 + n2*(g1 - 1)
local x = arr_x[g]
local y = arr_y[g]
local wvol = arr_wvol[g]
local Ni_0 = arr_Ni1_0[g1]*arr_Ni2_0[g2]
local Ni_u = arr_Ni1_s[g1]*arr_Ni2_0[g2]
local Ni_v = arr_Ni1_0[g1]*arr_Ni2_s[g2]
local gg = 4*g - 3
local jux = arr_jacobian[gg]
local gg = 4*g - 2
local jvx = arr_jacobian[gg]
local gg = 4*g - 1
local juy = arr_jacobian[gg]
local gg = 4*g
local jvy = arr_jacobian[gg]
local Ni_x = Ni_u*jux + Ni_v*jvx
local Ni_y = Ni_u*juy + Ni_v*jvy
contribution = Ni_0*wvol*f(x, y) + contribution
end
end
result_5805860847286743072 = contribution
return result_5805860847286743072

end

function kernel_a(arr_jacobian, arr_Ni1_0, arr_Ni1_s, arr_Ni1_ss, arr_Ni2_0, arr_Ni2_s, arr_Ni2_ss, arr_Nj1_0, arr_Nj1_s, arr_Nj1_ss, arr_Nj2_0, arr_Nj2_s, arr_Nj2_ss, arr_wvol, arr_x, arr_y, n1, n2, n_cols, n_rows)
setmetatable(_ENV, { __index=math })  


local n1 = math.floor(n1)
local n2 = math.floor(n2)
local n_cols = math.floor(n_cols)
local n_rows = math.floor(n_rows)
local contribution = 0.0
for g1 = 1, n1 do
for g2 = 1, n2 do
local g = g2 + n2*(g1 - 1)
local x = arr_x[g]
local y = arr_y[g]
local wvol = arr_wvol[g]
local Ni_0 = arr_Ni1_0[g1]*arr_Ni2_0[g2]
local Ni_u = arr_Ni1_s[g1]*arr_Ni2_0[g2]
local Ni_v = arr_Ni1_0[g1]*arr_Ni2_s[g2]
local Ni_uu = arr_Ni1_ss[g1]*arr_Ni2_0[g2]
local Ni_uv = arr_Ni1_s[g1]*arr_Ni2_s[g2]
local Ni_vv = arr_Ni1_0[g1]*arr_Ni2_ss[g2]
local Nj_0 = arr_Nj1_0[g1]*arr_Nj2_0[g2]
local Nj_u = arr_Nj1_s[g1]*arr_Nj2_0[g2]
local Nj_v = arr_Nj1_0[g1]*arr_Nj2_s[g2]
local Nj_uu = arr_Nj1_ss[g1]*arr_Nj2_0[g2]
local Nj_uv = arr_Nj1_s[g1]*arr_Nj2_s[g2]
local Nj_vv = arr_Nj1_0[g1]*arr_Nj2_ss[g2]
local gg = 4*g - 3
local jux = arr_jacobian[gg]
local gg = 4*g - 2
local jvx = arr_jacobian[gg]
local gg = 4*g - 1
local juy = arr_jacobian[gg]
local gg = 4*g
local jvy = arr_jacobian[gg]
local Ni_x = Ni_u*jux + Ni_v*jvx
local Ni_y = Ni_u*juy + Ni_v*jvy
local Ni_xx = Ni_uu
local Ni_xy = Ni_uv
local Ni_yy = Ni_vv
local Nj_x = Nj_u*jux + Nj_v*jvx
local Nj_y = Nj_u*juy + Nj_v*jvy
local Nj_xx = Nj_uu
local Nj_xy = Nj_uv
local Nj_yy = Nj_vv
contribution = contribution + wvol*(Ni_xx*Nj_xx + Ni_yy*Nj_yy)
end
end
result_5805860847286743072 = contribution
return result_5805860847286743072

end
