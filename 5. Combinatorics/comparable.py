# comparable.py
# From Classic Computer Science Problems in Python Chapter 2
# Copyright 2018 David Kopec
#
# Modified by Ariel Ortiz, 2022.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations
from typing import Any, Protocol, TypeVar

C = TypeVar('C', bound='Comparable')


class Comparable(Protocol):

    def __eq__(self, other: Any) -> bool:
        ...

    def __lt__(self: C, other: C) -> bool:
        ...

    def __le__(self: C, other: C) -> bool:
        return not other < self

    def __gt__(self: C, other: C) -> bool:
        return other < self

    def __ge__(self: C, other: C) -> bool:
        return not self < other
