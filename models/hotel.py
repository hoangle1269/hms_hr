from odoo import fields, models, api

class Hotel(models.Model):
    _name = "hotel.management"
    _description = "Hotel Management"

    hotel_ids = fields.Char(string="Hotel ID", unique=True, index=True)
    name = fields.Char(string="Hotel Name", required=True)
    address = fields.Char(string="Hotel Address", required=True)
    floor_count = fields.Integer(string="Number of Floors", required=True)
    room_count = fields.Integer(
        string="Number of Rooms",
        compute="_compute_room_count",
        store=True,
    )
    manager_id = fields.Many2one('hr.employee', string="Manager", domain="[('job_id', '=', 'Manager')]")
    employee_ids = fields.One2many('hr.employee', 'parent_id', string="Employees")
    user_id = fields.Many2one('res.users', string="User", related="manager_id.user_id", store=True)
    room_ids = fields.One2many(
        'hotel.room', 'hotel_id', string="Rooms"
    )

    _sql_constraints = [
    ('hotel_ids_unique', 'unique(hotel_ids)', 'Hotel id must be unique.')]

    @api.model
    def create(self, vals):
        if 'hotel_ids' not in vals:
            last_hotel = self.search([], order='hotel_ids desc', limit=1)
            if last_hotel:
                last_code = int(last_hotel.hotel_ids)
                new_code = str(last_code + 1)
            else:
                new_code = '1'
            vals['hotel_ids'] = new_code

        return super(Hotel, self).create(vals)

    @api.depends('room_ids')
    def _compute_room_count(self):
        for hotel in self:
            hotel.room_count = len(hotel.room_ids)
    
    @api.constrains('floor_count')
    def _onchange_floor_count(self):
        if self.floor_count < 1:
            raise models.ValidationError("Number of floors must be greater than 0.")