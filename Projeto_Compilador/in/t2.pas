program TestBinaryOp;

var
  a: integer;
  b: string;
  result: integer;

begin
  a := 10;
  b := 'hello';
  result := a + b;  { Invalid: cannot add integer and string }
  writeln(result);
end.