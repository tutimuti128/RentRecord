## Scope legend

Implemented = present in local code; browser acceptance is pending where stated in TASKS. Planned = product concept only.

| Stage | User action | Output | Status |
| --- | --- | --- | --- |
| Set up home | Enter tenancy, rent, deposit and landlord | Home record | Implemented; demo identity only |
| Move in | Add room photos, conditions and notes | Draft report | Implemented |
| Finalise | Lock report; later add dated notes | Fixed record plus addenda | Implemented |
| Everyday bills | Add/edit/delete bills; mark external payments and filter by due month | Monthly totals and overdue labels | Implemented; browser test pending |
| Local benefits | Browse sample offers; inspect category, location, terms and expiry | Fictional offer examples | Implemented as samples; not redeemable |
| Move out | Complete tasks and take room photos | Checklist and comparison | Implemented |
| Deposit | Explicitly record keys returned, request and outcome | Dated history | Implemented |
| Export | Open printable tenancy record | Print / Save as PDF | Implemented; output test pending |

Bills and local benefits are optional recurring branches during the tenancy; they do not block move-out. No payment is executed by the product. The deposit tracker starts through its own explicit action, separately from the move-out checklist.

## Editable diagram source

```mermaid
flowchart TD
    A["Create tenancy"] --> B["Move-in report"]
    B --> C["Finalise and retain record"]
    C --> D["During tenancy"]
    D --> E["Bills and monthly view · browser test pending"]
    D --> F["Sample local offers · fictional"]
    D --> G["Move-out checklist and photos"]
    E --> D
    F --> D
    G --> H["Compare apartment records"]
    H --> I["Track deposit"]
    I --> J["Export tenancy record"]
```

The bills and local-benefits screens are implemented in the current code. Their browser acceptance tests are still pending. Offers in the demo are fictional and not redeemable.
