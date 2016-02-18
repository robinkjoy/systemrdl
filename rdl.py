from rdl_lexer import RDLLexer
from rdl_parser import RDLParser

# Build the lexer
lexer = RDLLexer()
lexer.build()
tokens = lexer.tokens

# Test it out
data = '''
addrmap defaultid4489950 {
   reg {
      name = "data";
      desc = "Data read/write register";
      field {
         name = "data_field";
         desc = "Data read/write field";
         sw = rw;
         hw = r;
         reset = 32'b00000000000000000000000000000100;
         reset = 32'd2;
      } data_field[31:0];
   } data @0x0;
};
'''

#lexer.test(data)

parser = RDLParser()
root = parser.parse(data)
print (root.pprint())
