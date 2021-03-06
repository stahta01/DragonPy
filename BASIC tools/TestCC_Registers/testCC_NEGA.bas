1 CLS:PRINT "TEST CC WITH NEGA V0.3"
2 PRINT "(GPL V3 OR ABOVE)"
3 PRINT:PRINT "COPYLEFT 2013-2014 JENS DIEMER":PRINT
11 COUNT=15
20 LA=&H4000			' LOAD / EXECUTE ADDRESS
25 PRINT "POKE MACHINE CODE TO: $";HEX$(LA)
30 PA = LA			' START ADDRESS FOR POKE
50 READ HB$			' HEX CONSTANTS
60 IF HB$="END" THEN 100
65 V=VAL("&H"+HB$)
70 POKE PA,V	                ' POKE VALUE INTO MEMORY
75 'PRINT "POKE $";HEX$(V);" AT $";HEX$(PA)
80 PA = PA + 1			' INCREMENT POKE ADDRESS
90 GOTO 50
100 PRINT "LOADED, END ADDRESS IS: $"; HEX$(PA-1)
110 PRINT:INPUT "INPUT START VALUE (DEZ)";A$
115 IF A$="" THEN 20000 ELSE A=VAL(A$)
120 A=A-1
130 GOTO 500
140 PRINT "UP/DOWN OR ANYKEY FOR NEW VALUE";
150 I$ = INKEY$:IF I$="" THEN 150
160 IF I$=CHR$(&H5E) THEN A=A2-(COUNT*2) : GOTO 500 ' UP KEYPRESS
170 IF I$=CHR$(&H0A) THEN A=A2 : GOTO 500 ' DOWN KEYPRESS
180 GOTO 110 ' NOT UP/DOWN
500 CLS
550 FOR I = 1 TO COUNT
551 A2=(A+I) AND &HFF
552 'PRINT "SET A=";A2
553 POKE &H4500,A2 '  SET IN VALUE
560 EXEC LA '         RUN MACHINE CODE
570 CC=PEEK(&H4501) ' GET CC-REGISTER
580 A3=PEEK(&H4500) ' GET OUT VALUE
590 ' CREATE BITS
600 T = CC
610 B7$="E":IF T AND 128 THEN B7$="e"
620 B6$="F":IF T AND 64 THEN B6$="f"
630 B5$="H":IF T AND 32 THEN B5$="h"
640 B4$="I":IF T AND 16 THEN B4$="i"
650 B3$="N":IF T AND 8 THEN B3$="n"
660 B2$="Z":IF T AND 4 THEN B2$="z"
670 B1$="V":IF T AND 2 THEN B1$="v"
680 B0$="C":IF T AND 1 THEN B0$="c"
690 PRINT LEFT$(STR$(A2)+"  ",4);"> neg >";LEFT$(STR$(A3)+"  ",4);" cc=$";RIGHT$(" "+HEX$(CC),2);":";B7$;B6$;B5$;B4$;B3$;B2$;B1$;B0$
700 NEXT I
710 GOTO 140
1000 ' MACHINE CODE IN HEX
1010 ' LDA $4500
1020 DATA B6,45,00
1030 ' CLR,TFR TO CLEAR CC
1040 ' CLRB
1050 DATA 5F
1060 ' TFR B,CC
1070 DATA 1F,9A
1080 ' NEGA
1090 DATA 40
2000 ' TFR CC,B
2010 DATA 1F,A9
2020 ' STA $4500
2030 DATA B7,45,00
2040 ' STB $4501
2050 DATA F7,45,01
10000 ' RTS
10010 DATA 39
10020 DATA END
20000 PRINT:PRINT "BYE"
