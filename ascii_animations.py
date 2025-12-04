import os

'''
Spaceship

Globe

Tourists



'''

def build_animation(picture):
    for i in picture:
        print(i)

spaceship = [
"\n",
r"                     `. ___                                        ",
r"                    __,' __`.                _..----....____       ",
r"        __...--.'``;.   ,.   ;``--..__     .'    ,-._    _.-'      ",
r"  _..-''-------'   `'   `'   `'     O ``-''._   (,;') _,'          ",
r",'________________                          \`-._`-','             ",
r" `._              ```````````------...___   '-.._'-:               ",
r"    ```--.._      ,.                     ````--...__\-.            ",
r"            `.--. `-`                       ____    |  |`          ",
r"              `. `.                       ,'`````.  ;  ;`          ",
r"                `._`.        __________   `.      \'__/`           ",
r"                   `-:._____/______/___/____`.     \  `            ",
r"                               |       `._    `.    \              ",
r"                               `._________`-.   `.   `.___         ",
r"                                             SSt  `------'`        ",
"\n"
]



solar_system = [
"\n",
"\n"
r"                       :",
r"                       :",
r"                       :",
r"                       :",
r"        .              :",
r"         '.            :           .'",
r"           '.          :         .'",
r"             '.   .-''''''-.   .'                                   .'':",
r"               '.'          ''.'                               .-''''-.'         .---.          .----.        .-'''-.",
r"                :            :                _    _        .'     .' '.    ...'     '...    .'      '.    .'       '.",
r"        .........            .........    o  (_)  (_)  ()   :    .'    :   '..:.......:..'   :        :    :         :   o",
r"                :            :                              :  .'      :       '.....'       '.      .'    '.       .'",
r"                 :          :                             .'.'.      .'                        `''''`        `'''''`",
r"                  '........'                              ''   ``````",
r"                 .'    :   '.",
r"               .'      :     '.",
r"             .'        :       '.",
r"           .'          :         '.",
r"                       :",
r"                       :",
r"                       :",
r"                       :",

]

saturn = [
"\n",
"\n",
r"                                                                        ..;===+.",
r"                                                                .:=iiiiii=+=",
r"                                                             .=i))=;::+)i=+,",
r"                                                          ,=i);)I)))I):=i=;",
r"                                                       .=i==))))ii)))I:i++",
r"                                                     +)+))iiiiiiii))I=i+:'",
r"                                .,:;;++++++;:,.       )iii+:::;iii))+i='",
r"                             .:;++=iiiiiiiiii=++;.    =::,,,:::=i));=+'",
r"                           ,;+==ii)))))))))))ii==+;,      ,,,:=i))+=:",
r"                         ,;+=ii))))))IIIIII))))ii===;.    ,,:=i)=i+",
r"                        ;+=ii)))IIIIITIIIIII))))iiii=+,   ,:=));=,",
r"                      ,+=i))IIIIIITTTTTITIIIIII)))I)i=+,,:+i)=i+",
r"                     ,+i))IIIIIITTTTTTTTTTTTI))IIII))i=::i))i='",
r"                    ,=i))IIIIITLLTTTTTTTTTTIITTTTIII)+;+i)+i`",
r"                    =i))IIITTLTLTTTTTTTTTIITTLLTTTII+:i)ii:'",
r"                   +i))IITTTLLLTTTTTTTTTTTTLLLTTTT+:i)))=,",
r"                   =))ITTTTTTTTTTTLTTTTTTLLLLLLTi:=)IIiii;",
r"                  .i)IIITTTTTTTTLTTTITLLLLLLLT);=)I)))))i;",
r"                  :))IIITTTTTLTTTTTTLLHLLLLL);=)II)IIIIi=:",
r"                  :i)IIITTTTTTTTTLLLHLLHLL)+=)II)ITTTI)i=",
r"                  .i)IIITTTTITTLLLHHLLLL);=)II)ITTTTII)i+",
r"                  =i)IIIIIITTLLLLLLHLL=:i)II)TTTTTTIII)i'",
r"                +i)i)))IITTLLLLLLLLT=:i)II)TTTTLTTIII)i;",
r"              +ii)i:)IITTLLTLLLLT=;+i)I)ITTTTLTTTII))i;",
r"             =;)i=:,=)ITTTTLTTI=:i))I)TTTLLLTTTTTII)i;",
r"           +i)ii::,  +)IIITI+:+i)I))TTTTLLTTTTTII))=,",
r"         :=;)i=:,,    ,i++::i))I)ITTTTTTTTTTIIII)=+'",
r"       .+ii)i=::,,   ,,::=i)))iIITTTTTTTTIIIII)=+",
r"      ,==)ii=;:,,,,:::=ii)i)iIIIITIIITIIII))i+:'",
r"     +=:))i==;:::;=iii)+)=  `:i)))IIIII)ii+'",
r"   .+=:))iiiiiiii)))+ii;",
r"  .+=;))iiiiii)));ii+",
r" .+=i:)))))))=+ii+",
r".;==i+::::=)i=;",
r",+==iiiiii+,",
r"`+=+++;`",
]


