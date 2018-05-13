# def teste(fixado, *args):
#     for arg in args:
#         print(arg)
#
# lista = ['1','2','3']
# teste('paulo', 'rodrigo', 'foo', *lista)


def teste(fixado, **kwargs):
    for key in kwargs:
        print key +":"+str(kwargs[key])

tel = {'jack': 4098, 'sape': 4139}
teste(fixado='fix', **tel)

# minput = raw_input("digite: ")
# mlist = minput.split(",")
# print(mlist)
