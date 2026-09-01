local repository_root = "https://github.com/tjpools/embedding-geometry-lab/blob/main/book2/"
local current_section = "book-two"

local man_pages = {
  ["alignment"] = true,
  ["architecture-scales"] = true,
  ["attention"] = true,
  ["bayesian-update"] = true,
  ["callable-package"] = true,
  ["embedding-space"] = true,
  ["execution-trace"] = true,
  ["feed-forward"] = true,
  ["gradient-descent"] = true,
  ["jacobian"] = true,
  ["layer-norm"] = true,
  ["limits"] = true,
  ["man"] = true,
  ["memory-layout"] = true,
  ["recurrence"] = true,
  ["representation"] = true,
  ["residual"] = true,
  ["softmax"] = true,
  ["tensor"] = true,
  ["transformer-block"] = true,
}

function Header(element)
  if element.level ~= 1 then
    if element.identifier ~= "" then
      element.identifier = current_section .. "-" .. element.identifier
    end
    return element
  end

  local chapter = pandoc.utils.stringify(element.content):match("^Chapter%s+(%d+)")
  if chapter then
    element.identifier = "chapter-" .. tonumber(chapter)
  end
  current_section = element.identifier
  return element
end

function CodeBlock(element)
  local name = element.text:match("^([A-Z][A-Z0-9%-]*)%(")
  if name then
    return pandoc.Div(element, pandoc.Attr("man-" .. name:lower()))
  end
  return element
end

function Link(element)
  local chapter = element.target:match("^%.%./chapters/chapter_(%d+)%.md$")
  if chapter then
    element.target = "#chapter-" .. tonumber(chapter)
    return element
  end

  local man_page = element.target:match("^([%w%-]+)%.md$")
  if man_page and man_pages[man_page] then
    return pandoc.Span(element.content)
  end

  local artifact = element.target:match("^%.%./(evidence/.*)$")
    or element.target:match("^%.%./(visuals/.*%.md)$")
  if artifact then
    element.target = repository_root .. artifact
  end
  return element
end