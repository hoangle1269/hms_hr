# Hotel Management Module

## Overview
This module manages hotel-related operations including hotels, rooms, room features, bookings, employees, and user access. It ensures unique identifiers, relationships between entities, and proper permissions for different roles.

---

## Data Models

### 1. **Hotel Management**
- **Fields**:
  - Hotel Code (Unique)
  - Hotel Name
  - Hotel Address
  - Number of Floors
  - Number of Rooms (Auto-calculated based on associated rooms)
- **Requirements**:
  - Each hotel can have multiple rooms.
  - Room count is automatically calculated from the room list.

---

### 2. **Room Management**
- **Fields**:
  - Hotel (Reference to Hotel Management)
  - Hotel Address (Auto-filled from selected hotel)
  - Room Code (Unique per hotel)
  - Bed Type (Single, Double)
  - Room Price
  - Room Features (Many-to-Many relationship with Room Features Management)
  - Room Status (Available, Booked)
- **Requirements**:
  - Room code must be unique within a hotel.
  - Bed type options are restricted to "Single" or "Double".
  - Room status options are restricted to "Available" or "Booked".
  - A room can have multiple features.

---

### 3. **Room Features Management**
- **Fields**:
  - Feature Name (e.g., Mountain View, Two Windows)
- **Requirements**:
  - A feature can be associated with multiple rooms.

---

### 4. **Booking Management**
- **Fields**:
  - Booking Code
  - Customer Name
  - Booking Date (Default: Current date)
  - Hotel
  - Room Type
  - Room Code (Filtered based on hotel, room type, and availability)
  - Check-in Date
  - Check-out Date
  - Booking Status (New, Confirmed)
- **Requirements**:
  - Room selection is filtered by chosen hotel, room type, and availability.
  - Booking date defaults to the current date.
  - Check-in date cannot be after check-out date.
  - Initial booking status is "New".
  - Upon confirmation, booking status changes to "Confirmed".

---

### 5. **Employee Management (`hr.employee`)**
- Used for managing employees.
- Employees can belong to different roles (Employee, Manager, Admin).

---

### 6. **User Management (`res.users`)**
- Manages system login accounts.
- Employees can optionally have associated user accounts.

---

## Role-Based Permissions

### 1. **User Roles**:
- **Employee**: Basic access.
- **Manager**: Higher privileges than Employee.
- **Admin**: Full access.

### 2. **Permissions**:
| Module               | Employee       | Manager        | Admin         |
|-----------------------|----------------|----------------|---------------|
| Hotel Management      | Read           | Read           | Full          |
| Room Management       | Read           | Read           | Full          |
| Room Features         | Read           | Read           | Full          |
| Booking Management    | CRUD           | CRUD + Delete  | Full          |

---

## Record Rules

### 1. **Hotel Management**:
- Employee: View hotels where they are listed as staff.
- Manager: View hotels they manage.
- Admin: View all hotels.

### 2. **Room Management**:
- Employee: View rooms in their assigned hotel.
- Manager: View rooms in hotels they manage.
- Admin: View all rooms.

### 3. **Booking Management**:
- Employee: View bookings they created.
- Manager: View bookings in hotels they manage.
- Admin: View all bookings.

---

## Special Configurations

1. **Link Users with Employees**:
   - Users (`res.users`) must map to corresponding employees (`hr.employee`).
   - Use the HR module for employee management.

2. **Assign Managers to Hotels**:
   - Only employees with the Manager role can manage hotels.
   - One manager per hotel.
   - Display the manager and staff list on the hotel view.

---

## Key Features

1. **Automations**:
   - Auto-calculate room count for hotels.
   - Auto-fill hotel address for rooms.

2. **Dynamic Filters**:
   - Filter rooms in bookings by hotel, room type, and status.

3. **Validation Rules**:
   - Ensure unique codes for hotels and rooms.
   - Restrict field values (e.g., bed type, room status).

4. **Role Inheritance**:
   - Higher roles inherit permissions from lower roles (e.g., Admin > Manager > Employee).

---

## Reference
- [Odoo User Management Guide](https://www.odoo.com/documentation/18.0/vi/applications/general/users.html)
