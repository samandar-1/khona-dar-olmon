from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from db.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    username = Column(String)
    is_admin = Column(Boolean, default=False)

    ads = relationship("Ad", back_populates="user")
    ad_requests = relationship("AdRequest", back_populates="user")

class Ad(Base):
    __tablename__ = "ads"
    id = Column(Integer, primary_key=True, index=True)

    user_id = Cgit olumn(Integer, ForeignKey("users.id"))
    description = Column(String, nullable=False)

    type = Column(String, nullable=False)  # "gesucht" oder "angebot"
    kaltmiete = Column(Float, nullable=True)
    nebenkosten = Column(Float, nullable=True)
    raumflaeche = Column(Float, nullable=True)  # in m²

    stadt = Column(String, nullable=True)
    anmeldung_moeglich = Column(Boolean, default=False)

    vermietung_art = Column(String, nullable=False)  # "WG", "Wohnung", "Haus", "Parkplatz"

    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)

    bilder = Column(Text, nullable=True)  # JSON-String: ["file_id1","file_id2"]

    approved = Column(Boolean, default=False)
    telegram_message_id = Column(String, nullable=True)

    user = relationship("User")


# ----------------------------
# AdRequest Tabelle (Admin-Freigabe)
# ----------------------------
class AdRequest(Base):
    __tablename__ = "ad_requests"
    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    ad_id = Column(Integer, ForeignKey("ads.id"), nullable=True)  # falls Änderung einer bestehenden Anzeige
    action = Column(String, nullable=False)  # "create" oder "update"

    status = Column(String, default="pending")  # "pending", "approved", "rejected"

    user = relationship("User", back_populates="ad_requests")
