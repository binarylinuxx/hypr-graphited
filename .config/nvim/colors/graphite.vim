" ~/.config/nvim/colors/graphite.vim

" Clear existing highlights
highlight clear
if exists("syntax_on")
  syntax reset
endif

" Set theme name
let g:colors_name = "graphite"

" Base Colors (from your Kitty config)
let s:bg           = "#1E1E1E"  " color0 (darkest)
let s:bg_alt       = "#2B2B2B"  " background
let s:bg_highlight = "#3A3A3A"  " color1
let s:cursor_line  = "#4B4B4B"  " color2
let s:visual_select= "#5C5C5C"  " color3
let s:fg_dim       = "#7E7E7E"  " color5 (mid-gray)
let s:fg           = "#D1D1D1"  " foreground
let s:fg_light     = "#EEEEEE"  " color15 (lightest)
let s:comment_gray = "#A0A0A0"  " color7

" Basic UI
execute "highlight Normal       guifg=" . s:fg . " guibg=" . s:bg
execute "highlight NormalFloat  guifg=" . s:fg . " guibg=" . s:bg_alt
execute "highlight CursorLine   guibg=" . s:cursor_line . " gui=NONE"
execute "highlight LineNr       guifg=" . s:fg_dim
execute "highlight CursorLineNr guifg=" . s:fg_light . " gui=bold"
execute "highlight StatusLine   guifg=" . s:fg . " guibg=" . s:bg_alt . " gui=NONE"

" Syntax (monochrome)
execute "highlight Comment      guifg=" . s:comment_gray . " gui=italic"
execute "highlight Keyword      guifg=" . s:fg . " gui=bold"
execute "highlight String       guifg=" . s:fg
execute "highlight Identifier   guifg=" . s:fg
execute "highlight Function     guifg=" . s:fg . " gui=bold"

" Visual Mode
execute "highlight Visual       guibg=" . s:visual_select
execute "highlight Search       guifg=" . s:fg_light . " guibg=" . s:bg_highlight

" Diagnostics (no colors)
execute "highlight DiagnosticError guifg=" . s:fg_dim . " gui=undercurl"
execute "highlight DiagnosticWarn  guifg=" . s:comment_gray
