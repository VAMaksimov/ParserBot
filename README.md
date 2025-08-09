Below are 10 short practice tasks (each designed to be completed in ~15 minutes) aimed at an advanced C++ programmer. Each task includes a concise description, what you should implement or demonstrate, quick verification steps, and a brief hint. No full solutions included.

1) Deep copy vs shallow copy (raw pointer)
- Goal: Implement correct resource management for a small dynamic array class.
- Implement class IntArray:
  - Constructor IntArray(size_t n) allocating an int[].
  - Copy constructor + copy assignment implementing deep copy.
  - Destructor freeing memory.
  - operator[] and size().
- Tests:
  - Create IntArray a(3); set elements. Copy-construct b(a). Modify a[0] and verify b[0] is unchanged.
  - Assign c = a; modify a and verify c unchanged.
  - Check no double-free/crash (run under ASan if available).
- Hint: Use member initializer lists; follow RAII; handle self-assignment.

2) Const and reference members, copy assignment semantics
- Goal: Explore effects of const and reference members on copying and assignment.
- Implement class RefConstHolder:
  - Holds const int const_val and int& ref_val (reference bound via ctor).
  - Provide constructor taking (const int, int&).
  - Implement a copy constructor that preserves semantics you choose.
  - Provide copy assignment operator — decide whether to allow assignment or only copy values.
- Tests:
  - Show that default copy constructor copies const and reference (reference will refer to the same object).
  - Demonstrate that a defaulted assignment operator is ill-formed (references/const cannot be rebound). Implement operator= to copy the referenced integer's value instead of rebinding.
- Hint: Assignment cannot rebind references or reassign const members; implement operator= to copy the underlying values, or delete it intentionally.

3) Default member initializers and constructor precedence
- Goal: Show how in-class member initializers interact with constructors and initializer lists.
- Implement class Config:
  - Members with in-class defaults: int timeout = 30; std::string mode = "auto"; bool verbose = false;
  - Provide multiple constructors: default, Config(int timeout), Config(std::string mode, bool verbose).
  - In one constructor, explicitly initialize members in the member initializer list to different values.
- Tests:
  - Construct Config() and verify defaults.
  - Construct Config(10) and verify timeout=10, other defaults remain.
  - Construct Config("manual", true) and verify proper values.
  - Show that member initializer lists override in-class defaults for those members explicitly initialized.
- Hint: In-class initializers are used if the constructor doesn’t initialize that member.

4) Delegating constructors and central initialization
- Goal: Use delegating constructors to reduce duplication.
- Implement class Point3D:
  - Members double x,y,z with in-class defaults 0.
  - Provide constructors: Point3D(), Point3D(double xy), Point3D(double x,double y,double z).
  - Make 1-arg constructor delegate to 3-arg for convenience.
- Tests:
  - Instantiate with Point3D(), Point3D(1.0), Point3D(1,2,3) and verify values.
- Hint: Use delegating constructors to call a single centralized ctor.

5) Rule of five: make a move-only resource wrapper
- Goal: Implement type that is movable but not copyable.
- Implement class FileWrapper (or SocketWrapper):
  - Holds a resource handle (e.g., FILE* or a simulated int fd).
  - Delete copy constructor and copy assignment.
  - Implement move constructor and move assignment that transfer ownership.
  - Implement destructor that releases resource if owned.
- Tests:
  - Create wrapper w1 managing resource, move to w2 using std::move, confirm w1 no longer owns resource.
  - Attempt to copy — compilation should fail.
- Hint: Use =delete for copy ops, implement move ops carefully to null out source.

6) Observing copy/move (instrumented counters)
- Goal: Observe whether copy/move ctors are invoked in various contexts.
- Implement class Traceable:
  - Increment static counters in default, copy, move constructors, assignments, and destructor; also print messages optionally.
- Write small functions:
  - Traceable makeLocal(); // returns a local Traceable
  - Use: Traceable t = makeLocal();
  - Also: Traceable t2 = Traceable(); and Traceable t3 = std::move(t2);
- Tests:
  - Run and observe counter outputs to reason about copy elision/NRVO and move operations.
- Hint: Behavior depends on compiler and optimization; use prints or counters to inspect.

7) =default and =delete for special member functions
- Goal: Use =default and =delete to enforce intended semantics cleanly.
- Implement class NonCopyableButDefaultConstructible:
  - Default constructor defaulted.
  - Copy ctor and copy assignment deleted.
  - Move ctor and move assignment defaulted.
- Tests:
  - Default-construct object.
  - Move it (should compile).
  - Attempt to copy (should fail to compile).
- Hint: =default in-class gives you control without writing boilerplate.

8) Pimpl with unique_ptr (move-only or copyable)
- Goal: Implement a simple Pimpl (pointer-to-implementation) with correct special members.
- Implement class Widget:
  - Holds std::unique_ptr<Impl>.
  - Provide public constructors, destructor.
  - Decide whether Widget is movable only or also copyable (implement copy by deep-copying Impl).
- Tests:
  - Implement Widget::Widget(int) constructing Impl.
  - Make Widget movable by default (unique_ptr).
  - Optionally implement copy ctor that clones Impl for deep copy; test both behaviors.
- Hint: unique_ptr makes move automatic but prevents copy; implement clone() on Impl to support copy.

9) Aggregate initialization vs constructors
- Goal: Understand when brace initialization uses aggregate rules vs ctor overloads.
- Create struct S { int a; double b; std::string s; }; (no user-defined ctors).
- Create class T with same members but with a constructor T(int,double,std::string).
- Tests:
  - Initialize S s{1,2.0,"x"} and T t{1,2.0,"x"}; observe how each is constructed (aggregate init vs ctor).
  - Add a default member initializer to S and see behavior when using partial brace init.
- Hint: Aggregate initialization is available when there are no user-provided constructors, private/protected non-static data, or virtual functions.

10) Shared_ptr vs unique_ptr copying pitfalls
- Goal: Demonstrate differences between copying unique_ptr and shared_ptr and resource ownership semantics.
- Implement a small class ResourceHolder that holds either std::unique_ptr<int> or std::shared_ptr<int>.
- Tests:
  - For unique_ptr: show copying fails; moving transfers ownership.
  - For shared_ptr: copy increments use_count; modify underlying value through one holder and observe changes visible in others.
  - Examine lifetime: when all shared_ptrs are destroyed, resource freed.
- Hint: Use .use_count() for shared_ptr to inspect ownership count.

General tips for each task
- Keep each implementation small; compile with warnings enabled and optionally run under AddressSanitizer/Valgrind.
- Prefer initializer lists to initialize members (especially const/reference members).
- For tests, write a few assertions or simple prints to verify behavior.
- When you intend to prevent copying, prefer =delete over making functions private.

If you want, I can convert any one of these tasks into a short test suite or provide starter code (skeleton) for students to fill in. Which task would you like a starter file for?