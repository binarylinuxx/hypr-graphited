-- =============================================
-- 1. BOOTSTRAP lazy.nvim
-- =============================================
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git", "clone", "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

-- =============================================
-- 2. SETUP PLUGINS
-- =============================================
require("lazy").setup({
  -- Graphite theme
  {
    'kroucher/graphite.nvim',
    config = function()
      -- Set background to dark
      vim.opt.background = "dark"
      -- Apply the Graphite colorscheme
      -- vim.cmd.colorscheme("graphite")
    end
  },

  -- Lualine with Fish Tide-style sharp separators
  {
    "nvim-lualine/lualine.nvim",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      require('lualine').setup({
        options = {
          icons_enabled = true,
          theme = 'auto',
          component_separators = { left = '', right = ''},
          section_separators = { left = '', right = ''},
          disabled_filetypes = {
            statusline = {},
            winbar = {},
          },
          ignore_focus = {},
          always_divide_middle = true,
          always_show_tabline = true,
          globalstatus = false,
          refresh = {
            statusline = 100,
            tabline = 100,
            winbar = 100,
          }
        },
        sections = {
          lualine_a = {'mode'},
          lualine_b = {'branch', 'diff', 'diagnostics'},
          lualine_c = {'filename'},
          lualine_x = {'encoding', 'fileformat', 'filetype'},
          lualine_y = {'progress'},
          lualine_z = {'location'}
        },
        inactive_sections = {
          lualine_a = {},
          lualine_b = {},
          lualine_c = {'filename'},
          lualine_x = {'location'},
          lualine_y = {},
          lualine_z = {}
        },
        tabline = {},
        winbar = {},
        inactive_winbar = {},
        extensions = { "nvim-tree", "fugitive" }
      })
    end,
  },
})

-- =============================================
-- 3. UI SETTINGS (Fishy style!)
-- =============================================
vim.opt.termguicolors = true
vim.opt.showmode = false
vim.opt.laststatus = 3
vim.cmd.colorscheme("graphite")
vim.opt.guicursor = "n-v-c-sm:block-blinkwait300-blinkon200-blinkoff150"
