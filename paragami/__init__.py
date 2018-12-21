from paragami.pattern_containers import \
    PatternDict, PatternArray, \
    register_pattern_json, get_pattern_from_json, save_folded, load_folded
from paragami.numeric_array_patterns import NumericArrayPattern
from paragami.psdmatrix_patterns import PSDSymmetricMatrixPattern
from paragami.function_patterns import \
    FlattenFunctionInput, \
    FoldFunctionInput, \
    FoldFunctionOutput, \
    FoldFunctionInputAndOutput, \
    Functor
from paragami.simplex_patterns import SimplexArrayPattern
from paragami.optimization_lib import \
    PreconditionedFunction, \
    OptimizationObjective
from paragami.sensitivity_lib import \
    HyperparameterSensitivityLinearApproximation, \
    ParametricSensitivityTaylorExpansion, \
    LinearResponseCovariances
import paragami.autograd_supplement_lib

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
