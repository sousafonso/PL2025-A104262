program TestVariables;

var
  a,b,c,d,e: Integer;

begin
  { Use only a few variables }

  a := 100;
  b := 200;
  c := a + b;

  WriteLn('c = ', c);
end.