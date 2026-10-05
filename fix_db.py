import pathlib
p = pathlib.Path('app.py')
text = p.read_text(encoding='utf-8')
bad_str = '"postgresql://postgres.ygtkibauxgbrknsuzjzb:coldhearted%407218@://supabase.com"'
good_str = '"postgresql://postgres.ygtkibauxgbrknsuzjzb:coldhearted%407218@://supabase.com"'
p.write_text(text.replace(bad_str, good_str), encoding='utf-8')
print("Successfully fixed database string!")
