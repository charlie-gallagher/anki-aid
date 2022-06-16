import cli

btext = cli.blue("Blue text")
rtext = cli.red("Red text")
gcheck = cli.check("Successully downloaded!")
rex = cli.fail("Did not download the file")

check_b_combo = cli.check(f'Successully got {cli.blue("object")}')
h1_test_a = cli.h1('Short title')
h1_test_b = cli.h1('This is a longer title, but should be the same')


print(btext)
print(rtext)
print(gcheck)
print(rex)
print(check_b_combo)
print(h1_test_a)
print(h1_test_b)
