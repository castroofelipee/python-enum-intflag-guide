## Understanding Python IntFlag by Example
Everyone knows how annoying it can be to track multiple boolean states in a model, for example:

```python
  is_complete = Column(Boolean, default=False)
  verification_complete = Column(Boolean, default=False)
  is_admin = Column(Boolean, default=False)
```

Every time we want to add a new status, we usually need to add a new column and run a migration. But sometimes we just want to add new flags without changing the database schema.

For this, Python provides a very useful class in the `enum` module called `IntFlag`.

`IntFlag` is similar to Flag, but its members are also integers and can be used anywhere an integer is expected.

The idea is to store multiple boolean states inside a single integer using bits.

Basic Example
from enum import IntFlag, auto

```python
  class UserInfo(IntFlag):
      NONE = 0
      IS_VERIFIED = auto()
      IS_ADMIN = auto()
```

Now we can store these flags in a single integer column:

```python
  class UserTrack(Base):
      __tablename__ = "users"

      username = Column(String, nullable=False)
      flags = Column(Integer, default=UserInfo.NONE.value)

      def __str__(self):
          return f"Tracking of {self.username}"

      def add_flag(self, flag: UserInfo):
          self.flags |= flag

      def has_flag(self, flag: UserInfo) -> bool:
          return bool(self.flags & flag)
```

> Using auto() with IntFlag generates integer values that are powers of two:

```
IS_VERIFIED = 1   # 0001
IS_ADMIN    = 2   # 0010
```

Each flag represents one bit.

How It Works

Each flag is a binary value:

```
IS_VERIFIED = 1  # 0001
IS_ADMIN    = 2  # 0010
```

If a user has both flags, the stored value becomes:

```
0001 | 0010 = 0011  (which is 3)
```

So one integer can store many independent boolean states.

Working with Flags

We created this method:

```python
  def add_flag(self, flag):
      self.flags |= flag
```

Now we can do:

```
track.add_flag(UserInfo.IS_VERIFIED)
```

If the value was:

``` 
0000
```

It becomes:

```
0001
```

And later:

```
track.add_flag(UserInfo.IS_ADMIN)
```

Now it becomes:

```
0011
```

To check:
```python
track.has_flag(UserInfo.IS_ADMIN)  # True
track.has_flag(UserInfo.IS_VERIFIED)  # True
```


This article was inspired by cassiobotaro.de
