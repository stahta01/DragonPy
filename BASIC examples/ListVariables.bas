10 ' EXAMPLE VARIABLES:
20 SV=0:AV=0:EN=0:AD=0:I=0:V$=""
30 DIM A(0,1,2)
40 DIM BT$(10),Z(0),P$(1,1,1,1)
50 DIM EN(7,7)
60 '
70 SV=PEEK(27)*256+PEEK(28)
80 AV=PEEK(29)*256+PEEK(30)
90 EN=PEEK(31)*256+PEEK(32)
100 IF AV=SV THEN 170
110 PRINT "SIMPLE VARIABLES:"
120 AD=SV
130 GOSUB 300
140 PRINT V$
150 AD=AD+7
160 IF AD<AV THEN130
170 IF EN=AV THEN 280
180 PRINT"ARRAY VARIABLES:"
190 AD=AV
200 GOSUB 300
210 PRINT V$;"(";
220 FOR I=PEEK(AD+4) TO 1 STEP -1
230 PRINT PEEK(AD+I*2+3)*256+PEEK(AD+I*2+4);
240 NEXT
250 PRINT ")"
260 AD=AD+PEEK(AD+2)*256+PEEK(AD+3)
270 IF AD<EN THEN200
280 '
290 END
300 V$=CHR$(PEEK(AD)):I=PEEK(AD+1)
310 IF I AND 127 THEN V$=V$+CHR$(I AND 127)
320 IF I AND 128 THEN V$=V$+"$"
330 RETURN