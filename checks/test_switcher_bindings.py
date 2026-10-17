"""Portable migration checks; no Hyprland dispatch or real config writes."""
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import update


class BindingTests(unittest.TestCase):
    def setUp(self):self.block=(ROOT/'switcher-bindings.lua').read_text().strip()

    def test_stock_migration_is_idempotent_and_keeps_other_keys(self):
        text='local custom="keep"\nhl.bind("SUPER + Q", hl.dsp.exec_cmd("kitty"))\n'
        result=update.patch_switcher_bindings(text)
        self.assertIn(text,result);self.assertIn(self.block,result)
        self.assertEqual(update.patch_switcher_bindings(result),result)

    def test_custom_alt_tab_and_modifier_releases_are_preserved(self):
        for key in ['ALT + Tab','ALT + SHIFT + Tab','MOD1 + Tab','Alt_L','SHIFT + Alt_R']:
            with self.subTest(key=key):
                text='hl.bind("'+key+'", hl.dsp.exec_cmd("custom"))\n'
                self.assertEqual(update.patch_switcher_bindings(text),text)

    def test_dynamic_tab_binding_is_preserved_and_unrelated_tab_is_allowed(self):
        text='hl.bind(chosenMod .. " + Tab", hl.dsp.exec_cmd("custom"))\n'
        self.assertEqual(update.patch_switcher_bindings(text),text)
        text='hl.bind("SUPER + Tab", hl.dsp.exec_cmd("custom"))\n'
        self.assertIn(self.block,update.patch_switcher_bindings(text))

    def test_modified_owned_block_is_preserved(self):
        text=self.block.replace('window-next','my-action')+'\n'
        self.assertEqual(update.patch_switcher_bindings(text),text)

    def test_added_custom_binding_releases_our_unchanged_block(self):
        text=self.block+'\nhl.bind("ALT + Tab", hl.dsp.exec_cmd("custom"))\n'
        result=update.patch_switcher_bindings(text)
        self.assertNotIn('desktop-style window switcher begin',result)
        self.assertIn('hl.dsp.exec_cmd("custom")',result)

    def test_fresh_payload_matches_migration_block(self):
        self.assertIn(self.block,(ROOT/'payload/hypr/keybinds.lua').read_text())


if __name__=='__main__':unittest.main()
