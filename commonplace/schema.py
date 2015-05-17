import datetime as dt

from . import db

tags = db.Table("tags",
            db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
            db.Column("note_id", db.Integer, db.ForeignKey("note.id")))

class Note(db.Model):
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String, nullable=False, unique=True)
    text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String, nullable=False, default="misc")

    created = db.Column(db.DateTime, nullable=False, default=dt.datetime.now)
    updated = db.Column(db.DateTime, nullable=False, default=dt.datetime.now,
                        onupdate=dt.datetime.now)

    source = db.Column(db.String, nullable=True)
    fpath = db.Column(db.String, nullable=True, unique=True)

    tags = db.relationship("Tag", secondary=tags,
                           backref=db.backref("notes", lazy="dynamic"))

class Tag(db.Model):
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, index=True)

class Annotation(db.Model):
    __tablename__ = "annotation"

    id = db.Column(db.Integer, primary_key=True)

    created = db.Column(db.DateTime, nullable=False, default=dt.datetime.now)
    updated = db.Column(db.DateTime, nullable=False, default=dt.datetime.now,
                        onupdate=dt.datetime.now)

    src_id = db.Column(db.Integer, db.ForeignKey("note.id"), index=True)
    dest_id = db.Column(db.Integer, db.ForeignKey("note.id"), nullable=True)

    number = db.Column(db.Integer, index=True)
    text = db.Column(db.Text)

    src = db.relationship("Note", foreign_keys=src_id,
                          backref=db.backref("outgoing"))
    dest = db.relationship("Note", foreign_keys=dest_id,
                           backref=db.backref("incoming"))
