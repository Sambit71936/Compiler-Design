import lexical
import syntax
import semantic
import intermediate
import optimization
import targe

print("\n=========== MINI COMPILER STARTED ===========")

lexical.run_lexical()
syntax.run_syntax()
semantic.run_semantic()
intermediate.run_intermediate()
optimization.run_optimization()
targe.run_targe()

print("\n=========== COMPILER FINISHED ===========")
