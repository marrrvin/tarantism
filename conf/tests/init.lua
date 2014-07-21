
function clear_space(space)
    space = tonumber(space)

    if box.space[space] ~= nil then
        box.space[space]:truncate()
    end
end
