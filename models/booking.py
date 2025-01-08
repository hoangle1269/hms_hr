from odoo import models, fields, api
from datetime import date

class BookingOrder(models.Model):
    _name = 'booking.order'
    _description = 'Booking Order'

    booking_code = fields.Char(string="Booking Code", unique=True)
    customer_name = fields.Char(string="Customer Name", required=True)
    booking_date = fields.Date(string="Booking Date", default=date.today(), required=True)
    check_in_date = fields.Date(string="Check-in Date", required=True)
    check_out_date = fields.Date(string="Check-out Date", required=True)
    hotel_id = fields.Many2one('hotel.management', string="Hotel", required=True)
    room_type = fields.Selection([
        ('single', 'Single Bed'),
        ('double', 'Double Bed')
    ], string="Room Type", required=True)
    room_id = fields.Many2one(
        'hotel.room',
        string="Room ID",
        required=True,
        domain="[('hotel_id', '=', hotel_id),('bed_type', '=', room_type),('state', '=', 'confirmed')]"
    )
    room_name = fields.Char(string="Room Name", related="room_id.room_code", store=True)
    state = fields.Selection([
        ('new', 'New'),
        ('confirmed', 'Confirmed')
    ], string="Booking Status", default='new', required=True)

    @api.model
    def create(self, vals):
        if 'booking_code' not in vals:
            last_booking = self.search([], order='booking_code desc', limit=1)
            if last_booking:
                last_code = int(last_booking.booking_code)
                new_code = str(last_code + 1)
            else:
                new_code = '1'
            vals['booking_code'] = new_code
        room = self.env['hotel.room'].browse(vals['room_id'])
        if room:
            overlap_booking = self.env['booking.order'].search([
                ('room_id', '=', vals['room_id']),
                ('check_in_date', '<=', vals['check_out_date']),
                ('check_out_date', '>=', vals['check_in_date']),
              ])
            if overlap_booking:
                raise models.ValidationError("The room is already booked for the selected dates.")

        room.state = 'booked'
        return super(BookingOrder, self).create(vals)

    # Constraints
    @api.constrains('check_in_date', 'check_out_date')
    def _check_dates(self):
        for record in self:
            if record.check_in_date > record.check_out_date:
                raise models.ValidationError("Check-in date cannot be later than check-out date.")

    @api.depends('room_id')
    def _compute_room_code(self):
        for record in self:
            if record.room_id:
                record.room_code = record.room_id.room_code

    def unlink(self):
        for record in self:
            if record.room_id:
                other_bookings = self.search([
                    ('room_id', '=', record.room_id.id),
                    ('id', '!=', record.id)  # Loại bỏ bản ghi hiện tại
                ])
                if not other_bookings:
                    record.room_id.state = 'available'
        return super(BookingOrder, self).unlink()

