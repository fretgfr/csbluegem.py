csbluegem package
===============

csbluegem.client module
---------------------
.. currentmodule:: csbluegem.client

.. autoclass:: csbluegem.client.Client
   :members:
   :show-inheritance:


csbluegem.types module
---------------------

.. currentmodule:: csbluegem.types

.. autoclass:: csbluegem.types.Screenshots
   :members:
   :show-inheritance:

.. autoclass:: csbluegem.types.PatternDataScreenshots
   :members:
   :show-inheritance:

.. autoclass:: csbluegem.types.PatternDataExtra
   :members:
   :show-inheritance:

.. autoclass:: csbluegem.types.PatternData
   :members:
   :show-inheritance:

.. autoclass:: csbluegem.types.SearchMeta
   :members:
   :show-inheritance:

.. autoclass:: csbluegem.types.Sale
   :members:
   :show-inheritance:

.. autoclass:: csbluegem.types.SearchResponse
   :members:
   :show-inheritance:

.. autoclass:: csbluegem.types.PatternDataResponse
   :members:
   :show-inheritance:

.. class:: Origin

    Where a :class:`~csbluegem.types.Sale` originated from.

   .. attribute:: Buff

       Buff.163.com
   .. attribute:: CSFloat

       CSFloat.com
   .. attribute:: SkinBid

       SkinBid.com
   .. attribute:: BroSkins

       BroSkins.com

.. class:: FilterType

   What a :class:`~csbluegem.types.Filter` should filter by.

   .. attribute:: PlaysideBlue

       The amount of blue on the play side of the item.
   .. attribute:: PlaysidePurple

       The amount of purple on the play side of the item.
   .. attribute:: PlaysideGold

       The amount of gold on the play side of the item.
   .. attribute:: BacksideBlue

       The amount of blue on the back side of the item.
   .. attribute:: BacksidePurple

       The amount of purple on the back side of the item.
   .. attribute:: BacksideGold

       The amount of gold on the back side of the item.

.. autoclass:: csbluegem.types.Filter
   :members:
   :show-inheritance:

.. class:: Order

   How results from the API should be ordered.

   .. attribute:: Asc

       Sort in ascending order.
   .. attribute:: Desc

       Sort in descending order.

.. class:: ItemType

   The type of an item.

   .. attribute:: StatTrak

       A StatTrak item.
   .. attribute:: Normal

       A non StatTrak item.

.. class:: Currency

   Available currencies for use in the API."

   .. attribute:: USD

       United States Dollar
   .. attribute:: EUR

       Euros
   .. attribute:: JPY
       Japanese Yen

   .. attribute:: GBP
       Great British Pound

   .. attribute:: CNY
       Chinese Yuan

   .. attribute:: AUD
       Australian Dollar

   .. attribute:: CAD
       Canadian Dollar

.. class:: SortKey

   How the results of a query should be sorted.

   .. attribute:: PlaysideBlue

       The amount of blue on the play side.
   .. attribute:: PlaysidePurple

       The amount of purple on the play side.
   .. attribute:: PlaysideGold

       The amount of gold on the play side.
   .. attribute:: BacksideBlue

       The amount of blue on the back side.
   .. attribute:: BacksidePurple

       The amount of purple on the back side.
   .. attribute:: BacksideGold

       The amount of gold on the back side.
   .. attribute:: PlaysideContourBlue

       The number of blue regions on the play side.
   .. attribute:: PlaysideContourPurple

       The number of purple regions on the play side.
   .. attribute:: BacksideContourBlue

       The number of blue regions on the back side.
   .. attribute:: BacksideContourPurple

       The number of purple regions on the back side.
   .. attribute:: PatternData

       The pattern of the item.
   .. attribute:: Float

       The float of the item.
   .. attribute:: Date

       The date of the sale.
   .. attribute:: Price

       The price of the sale.

.. class:: BlueGemItem

   Items that can be queried from the API.

   .. attribute:: AK47

       AK-47
   .. attribute:: Bayonet

       Bayonet Knife
   .. attribute:: BowieKnife

       Bowie Knife
   .. attribute:: ButterflyKnife

       Butterfly Knife
   .. attribute:: ClassicKnife

       Classic Knife
   .. attribute:: FalchionKnife

       Falchion Knife
   .. attribute:: FiveSeveN

       Five-SeveN
   .. attribute:: FlipKnife

       Flip Knife
   .. attribute:: GutKnife

       Gut Knife
   .. attribute:: HuntsmanKnife

       Huntsman Knife
   .. attribute:: HydraGloves

       Hydra Gloves
   .. attribute:: Karambit

       Karambit Knife
   .. attribute:: KukriKnife

       Kukri Knife
   .. attribute:: M9Bayonet

       M9 Bayonet Knife
   .. attribute:: MAC10

       MAC-10
   .. attribute:: NavajaKnife

       Navaja Knife
   .. attribute:: NomadKnife

       Nomad Knife
   .. attribute:: ParacordKnife

       Paracord Knife
   .. attribute:: ShadowDaggers

       Shadow Daggers
   .. attribute:: SkeletonKnife

       Skeleton Knife
   .. attribute:: StilettoKnife

       Stiletto Knife
   .. attribute:: SurvivalKnife

       Survival Knife
   .. attribute:: TalonKnife

       Talon Knife
   .. attribute:: UrsusKnife

       Ursus Knife

.. class:: BlueGemKnife

   Knives that can be queried from the API.

   .. attribute:: Bayonet

       Bayonet Knife
   .. attribute:: BowieKnife

       Bowie Knife
   .. attribute:: ButterflyKnife

       Butterfly Knife
   .. attribute:: ClassicKnife

       Classic Knife
   .. attribute:: FalchionKnife

       Falchion Knife
   .. attribute:: FlipKnife

       Flip Knife
   .. attribute:: GutKnife

       Gut Knife
   .. attribute:: HuntsmanKnife

       Huntsman Knife
   .. attribute:: Karambit

       Karambit Knife
   .. attribute:: KukriKnife

       Kukri Knife
   .. attribute:: M9Bayonet

       M9 Bayonet Knife
   .. attribute:: NavajaKnife

       Navaja Knife
   .. attribute:: NomadKnife

       Nomad Knife
   .. attribute:: ParacordKnife

       Paracord Knife
   .. attribute:: ShadowDaggers

       Shadow Daggers
   .. attribute:: SkeletonKnife

       Skeleton Knife
   .. attribute:: StilettoKnife

       Stiletto Knife
   .. attribute:: SurvivalKnife

       Survival Knife
   .. attribute:: TalonKnife

       Talon Knife
   .. attribute:: UrsusKnife

       Ursus Knife


csbluegem.utils module
--------------------

.. currentmodule:: csbluegem.utils

.. autofunction:: csbluegem.utils.utcnow

.. autofunction:: csbluegem.utils.as_chunks

.. autofunction:: csbluegem.utils.safe_get


csbluegem.errors module
---------------------

.. currentmodule:: csbluegem.errors

.. autoclass:: csbluegem.errors.BlueGemError
    :members:
    :show-inheritance:

.. autoclass:: csbluegem.errors.BadArgument
    :members:
    :show-inheritance:

.. autoclass:: csbluegem.errors.HTTPException
    :members:
    :show-inheritance:

.. autoclass:: csbluegem.errors.NotFound
    :members:
    :show-inheritance:

.. autoclass:: csbluegem.errors.ServerError
    :members:
    :show-inheritance:

.. autoclass:: csbluegem.errors.InvalidRequest
    :members:
    :show-inheritance:
