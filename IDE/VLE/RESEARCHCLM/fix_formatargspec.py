"""
Fix for formatargspec compatibility with Python 3.11
"""

import inspect
import astor

# Add formatargspec back to inspect module
if not hasattr(inspect, 'formatargspec'):
    def formatargspec(args, varargs=None, varkw=None, defaults=None,
                     kwonlyargs=(), kwonlydefaults=None, annotations=None,
                     formatarg=str, formatvarargs=lambda name: '*' + name,
                     formatvarkw=lambda name: '**' + name,
                     formatvalue=lambda value: '=' + repr(value),
                     formatreturns=lambda text: ' -> ' + text,
                     formatannotation=lambda text: ': ' + text):
        """Replacement for inspect.formatargspec in Python 3.11+"""
        return astor.formatargspec(args, varargs, varkw, defaults,
                                 kwonlyargs, kwonlydefaults, annotations,
                                 formatarg, formatvarargs, formatvarkw,
                                 formatvalue, formatreturns, formatannotation)
    
    inspect.formatargspec = formatargspec
    print("✅ formatargspec compatibility patch applied!")

print("🔧 Compatibility fix loaded!")


