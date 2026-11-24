OPENQASM 3.0;
include "stdgates.inc";

bit[4] c;
qubit[4] q;

// test input a=1, b=1
x q[0];
x q[1];

// Half Adder
cx q[0], q[2];      // sum = a XOR b
cx q[1], q[2];
ccx q[0], q[1], q[3]; // carry = a AND b


c[0] = measure q[0];
c[1] = measure q[1];
c[2] = measure q[2];
c[3] = measure q[3];