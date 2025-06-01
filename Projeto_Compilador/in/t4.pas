program TestSumMulZeroOne;

var
  a, b, c: Integer;

begin
  // Test sum with 0
  a := 0; b := 5;
  c:= 0 + b;

  a := 3; b := 0;
  c:= a + 0;

  // Test multiplication with 0
  a := 0; b := 7;
  c:= 0 * b;

  a := 4; b := 0;
  c:= a * 0;

  // Test multiplication with 1
  a := 1; b := 9;
  c:=1 * b;

  a := 8; b := 1;
  c:=a * 1;
end.