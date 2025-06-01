program TestComparisonsAndLogicLiterals;

begin
  //writeln(10 = 20);        // False
  writeln(10 <> 20);      // True
  writeln(10 < 20);        // True
  writeln(10 <= 20);      // True
  writeln(10 > 20);        // False
  writeln(10 >= 20);      // False

  writeln(True and False);   // False
  writeln(True or False);     // True
end.