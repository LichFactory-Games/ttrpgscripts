function TableToTableStar(elem)
    if elem.t == 'Table' then
        local captionText = ""

        -- Determine the number of columns dynamically
        local max_cols = 0
        for _, row in ipairs(elem.bodies[1].body) do
            max_cols = math.max(max_cols, #row.cells)
        end
        local column_spec = string.rep("l ", max_cols)  -- Construct column spec based on the max columns

        -- Extract table caption if available and set the caption
        if elem.caption and elem.caption.long and #elem.caption.long > 0 then
            captionText = pandoc.utils.stringify(elem.caption.long)
        end

        local rows = {}

        -- Process the table headers if present
        if elem.head and elem.head.rows then
            for _, row in ipairs(elem.head.rows) do
                local header_cells = {}
                for _, cell in ipairs(row.cells) do
                    if cell.content then
                        local cell_content = pandoc.utils.blocks_to_inlines(cell.content)
                        local header_text = pandoc.utils.stringify(cell_content)
                        table.insert(header_cells, header_text)
                    end
                end
                table.insert(rows, table.concat(header_cells, ' & '))
            end
        end

        -- Process the table body
        if elem.bodies then
            for _, body in ipairs(elem.bodies) do
                for _, row in ipairs(body.body) do
                    local body_cells = {}
                    for _, cell in ipairs(row.cells) do
                        if cell.content then
                            local cell_content = pandoc.utils.blocks_to_inlines(cell.content)
                            local cell_text = pandoc.utils.stringify(cell_content)
                            table.insert(body_cells, cell_text)
                        end
                    end
                    table.insert(rows, table.concat(body_cells, ' & '))
                end
            end
        end

        local table_content = "\\toprule\n"
        for _, row in ipairs(rows) do
            table_content = table_content .. row .. " \\\\\n"
        end
        table_content = table_content .. "\\bottomrule"

        local new_elem_content = '\\begin{table}[H]\n'
        if captionText ~= "" then
            new_elem_content = new_elem_content .. '\\caption{' .. captionText .. '}\n'
        end
        new_elem_content = new_elem_content .. '\\begin{tabular}{' .. column_spec .. '}\n' .. table_content .. '\\end{tabular}\n\\end{table}'

        local new_elem = pandoc.RawBlock('latex', new_elem_content)
        return new_elem
    end
end

return {
    {Table = TableToTableStar}
}
