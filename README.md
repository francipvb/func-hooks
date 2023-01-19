# Func hooks

Hooks for python functions.

## Motivation:

I am developing a system with a microservices architecture and I want to add event hooks to some methods.

However, I don't want to add unrelated code to the busines logic methods. Because this, I developed this package, to be able to add execution points to a particular function.

## Example usage:

```python
>>> import func_hooks
>>> @func_hooks.hooks
... def my_func():
...     print("Ran my_func")
...
>>> @my_func.on_before
... def _run_before(invocation):
...     print("Running before my_func.")
...
>>> @my_func.on_after
... def _run_before(invocation_result):
...     print("Running after my_func.")
...
>>> my_func()
Running before my_func.
Ran my_func
Running after my_func.
>>>
```
