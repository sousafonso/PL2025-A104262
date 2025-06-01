program TestIfElse;
var
  a, b, c,x,y: integer;
// E esperado imprimir 2 e 2
begin
  a := 1;
  b := 2;
  c := 3;
  x := 1;
  y := 2;
  
  writeln('Teste 1');
  if a = 1 then
    if b = 2 then
      if c = 4 then
        writeln('Errado')
      else
        writeln('Correto')
  else
    writeln('Errado');

  writeln('Teste 2');
  if x = 3 then
    begin
      if y = 2 then
        writeln('Errado');
    end
  else
    writeln('Correto');
end.