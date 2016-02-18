import ply.yacc as yacc
from rdl_lexer import RDLLexer
import rdl_ast

class RDLParser():

    def __init__(self):

        self.rdllexer = RDLLexer()
        self.rdllexer.build()
        self.tokens = self.rdllexer.tokens
        self.rdlparser = yacc.yacc(module=self)

    def parse(self, text):
        return self.rdlparser.parse(
                input=text,
                lexer=self.rdllexer)

    def p_root(self, p):
      'root : component_def'
      p[0] = p[1]

    def p_component_def_0(self, p):
      'component_def : component_specifier ID LBRACE component_content RBRACE SEMI'
      p[0] = rdl_ast.Component(p[1], p[2], p[4])

    def p_component_def_1(self, p):
      'component_def : component_specifier LBRACE component_content RBRACE ID SEMI'
      p[0] = rdl_ast.ComponentInst(p[1], p[5], p[3])

    def p_component_def_2(self, p):
      'component_def : component_specifier LBRACE component_content RBRACE ID anonymous_component_inst_elems SEMI'
      p[0] = rdl_ast.ComponentInst(p[1], p[5], p[3])

    def p_anonymous_component_inst_elems(self, p):
      '''anonymous_component_inst_elems : AT NUM
                                        | array
                                        '''

    def p_array(self, p):
      '''array : LSQ NUM COLON NUM RSQ
               | LSQ NUM RSQ
               '''

    def p_component_content_1(self, p):
      'component_content : component_def'
      p[0] = [p[1]]

    def p_component_content_2(self, p):
      'component_content : component_content component_def'
      p[0] = p[1] + [p[2]]

    def p_component_content_3(self, p):
      'component_content : property_assign'
      p[0] = [p[1]]

    def p_component_content_4(self, p):
      'component_content : component_content property_assign'
      p[0] = p[1] + [p[2]]

    def p_property_assign(self, p):
      'property_assign : property_specifier EQ property_value SEMI'
      p[0] = rdl_ast.Property(p[1], p[3])

    def p_component_specifier(self, p):
      '''component_specifier : ADDRMAP
                             | REG
                             | REGFILE
                             | FIELD
                             | REF
                             '''
      p[0] = p[1]

    def p_property_specifier(self, p):
      '''property_specifier : NAME
                            | DESC
                            | ARBITER
                            | RSET
                            | RCLR
                            | WOCLR
                            | WOSET
                            | WE
                            | WEL
                            | SWWE
                            | SWWEL
                            | HWSET
                            | HWCLR
                            | SWMOD
                            | SWACC
                            | STICKY
                            | STICKYBIT
                            | INTR
                            | ANDED
                            | ORED
                            | XORED
                            | COUNTER
                            | OVERFLOW
                            | SHAREDEXTBUS
                            | ERREXTBUS
                            | RESET
                            | LITTLEENDIAN
                            | BIGENDIAN
                            | RSVDSET
                            | RSVDSETX
                            | BRIDGE
                            | SHARED
                            | MSB0
                            | LSB0
                            | SYNC
                            | ASYNC
                            | CPUIF_RESET
                            | FIELD_RESET
                            | ACTIVEHIGH
                            | ACTIVELOW
                            | SINGLEPULSE
                            | UNDERFLOW
                            | INCR
                            | DECR
                            | INCRWIDTH
                            | DECRWIDTH
                            | INCRVALUE
                            | DECRVALUE
                            | SATURATE
                            | DECRSATURATE
                            | THRESHOLD
                            | DECRTHRESHOLD
                            | DONTCOMPARE
                            | DONTTEST
                            | INTERNAL
                            | ALIGNMENT
                            | REGWIDTH
                            | FIELDWIDTH
                            | SIGNALWIDTH
                            | ACCESSWIDTH
                            | SW
                            | HW
                            | ADDRESSING
                            | PRECEDENCE
                            | ENCODE
                            | RESETSIGNAL
                            | CLOCK
                            | MASK
                            | ENABLE
                            | HWENABLE
                            | HWMASK
                            | HALTMASK
                            | HALTENABLE
                            | HALT
                            | NEXT
                '''
      p[0] = p[1]

    def p_property_value(self, p):
      '''property_value : _BOOL
                        | RW
                        | WR
                        | R
                        | W
                        | NA
                        | COMPACT
                        | REGALIGN
                        | FULLALIGN
                        | HW
                        | SW
                        | NUM
                        | WNUM
                        | STR
                        '''
      p[0] = p[1]

    def p_error(self, p):
        print ("Parse error at '%s'" % p.value)

