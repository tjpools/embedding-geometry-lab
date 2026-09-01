```text
CALLABLE-PACKAGE(8)              Book Two Man Pages             CALLABLE-PACKAGE(8)

NAME
       callable-package - validated serialized model bound to a runtime and interface

SYNOPSIS
       load(package) -> PACKAGE_VALID | error_code
       construct(spec, params, op, runtime) -> callable
       callable(request) -> response

DESCRIPTION
       A package binds four contract-bearing sections: manifest (format,
       required runtime capability), architecture (identity, version,
       operation, dimensions), parameters (weights, bias), and interface
       (request/response schema). A loader validates required fields,
       declared dimensions against payload shapes, framework operation
       availability, runtime capability, and interface schemas, in that
       order, before constructing a callable object. Reloading an identical
       package and resending an identical request reproduces identical
       results.

NOTES
       An architecture specification is not an executable; a package on disk
       is not an in-memory object; a framework supporting an operation does
       not mean a specific package is valid. A dimension mismatch is rejected
       before construction, with zero downstream invocations - failure does
       not hide inside a later arithmetic exception. This page does not
       measure latency, throughput, or hardware utilization, and claims no
       compatibility with any real model-serialization format.

SEE ALSO
       transformer-block(8), alignment(7)

SOURCE
       Chapter 12, callable-tool probe.
```
