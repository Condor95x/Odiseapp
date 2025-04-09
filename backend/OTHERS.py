{'''
    # Rutas para Insumos
    @router.get("/insumos", response_model=List[Insumo])
    def leer_insumos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
        insumos = obtener_insumos(db, skip, limit)
        return insumos

    @router.post("/insumos", status_code=status.HTTP_201_CREATED, response_model=Insumo)
    def crear_insumo(insumo: InsumoCreate, db: Session = Depends(get_db)):
        db_insumo = crear_insumo(db, insumo)
        return db_insumo

    # ... (Rutas para Insumos - get_insumo, actualizar_insumo, eliminar_insumo)

    # Rutas para DetallesInsumosConsumidos
    @router.get("/detalles_insumos_consumidos", response_model=List[DetalleInsumoConsumido])
    def leer_detalles_insumos_consumidos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
        detalles = obtener_detalles_insumos_consumidos(db, skip, limit)
        return detalles

    @router.post("/detalles_insumos_consumidos", status_code=status.HTTP_201_CREATED, response_model=DetalleInsumoConsumido)
    def crear_detalle_insumo_consumido(detalle: DetalleInsumoConsumidoCreate, db: Session = Depends(get_db)):
        db_detalle = crear_detalle_insumo_consumido(db, detalle)
        return db_detalle

    # ... (Rutas para DetallesInsumosConsumidos - get_detalle_insumo, actualizar_detalle_insumo, eliminar_detalle_insumo)

    # Rutas para Usuarios
    @router.get("/usuarios", response_model=List[UsuarioRead])
    def leer_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
        usuarios = obtener_usuarios(db, skip, limit)
        return usuarios

    @router.post("/usuarios", status_code=status.HTTP_201_CREATED, response_model=UsuarioRead)
    def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
        db_usuario = crear_usuario(db, usuario)
        return db_usuario

    # ... (Rutas para Usuarios - get_usuario, actualizar_usuario, eliminar_usuario)

    from models import Operacion,Insumo,DetalleInsumoConsumido,Usuario

    -----------------------------------------
    CRUD OTHERS

    # -----------------------------------
    # 📌 CRUD PARA INSUMOS
    # -----------------------------------

    # 🔹 Obtener lista de insumos
    def obtener_insumos(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Insumo).offset(skip).limit(limit).all()

    # 🔹 Crear un nuevo insumo
    def crear_insumo(db: Session, insumo: InsumoCreate):
        nuevo_insumo = Insumo(**insumo.dict())
        db.add(nuevo_insumo)
        db.commit()
        db.refresh(nuevo_insumo)
        return nuevo_insumo

    # 🔹 Obtener un insumo por ID
    def obtener_insumo(db: Session, insumo_id: int):
        insumo = db.query(Insumo).filter(Insumo.id == insumo_id).first()
        if not insumo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Insumo no encontrado")
        return insumo

    # 🔹 Actualizar un insumo
    def actualizar_insumo(db: Session, insumo_id: int, insumo_update: dict):
        insumo = obtener_insumo(db, insumo_id)

        for key, value in insumo_update.dict(exclude_unset=True).items():
            setattr(insumo, key, value)

        db.commit()
        db.refresh(insumo)
        return insumo

    # 🔹 Eliminar un insumo
    def eliminar_insumo(db: Session, insumo_id: int):
        insumo = obtener_insumo(db, insumo_id)
        db.delete(insumo)
        db.commit()
        return {"message": "Insumo eliminado"}

    # -----------------------------------
    # 📌 CRUD PARA DETALLES DE INSUMOS CONSUMIDOS
    # -----------------------------------

    # 🔹 Obtener lista de detalles de insumos consumidos
    def obtener_detalles_insumos_consumidos(db: Session, skip: int = 0, limit: int = 10):
        return db.query(DetalleInsumoConsumido).offset(skip).limit(limit).all()

    # 🔹 Crear un nuevo detalle de insumo consumido
    def crear_detalle_insumo_consumido(db: Session, detalle: DetalleInsumoConsumidoCreate):
        nuevo_detalle = DetalleInsumoConsumido(**detalle.dict())
        db.add(nuevo_detalle)
        db.commit()
        db.refresh(nuevo_detalle)
        return nuevo_detalle

    # -----------------------------------
    # 📌 CRUD PARA USUARIOS
    # -----------------------------------

    # 🔹 Obtener lista de usuarios
    def obtener_usuarios(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Usuario).offset(skip).limit(limit).all()

    # 🔹 Obtener un usuario por ID
    def obtener_usuario(db: Session, usuario_id: int):
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        return usuario

    # 🔹 Crear un nuevo usuario (con encriptación de contraseña)
    def crear_usuario(db: Session, usuario: UsuarioCreate):
        hashed_password = pwd_context.hash(usuario.password)  # 🔒 Encriptar la contraseña
        nuevo_usuario = Usuario(
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            email=usuario.email,
            rol=usuario.rol,
            fecha_creacion=usuario.fecha_creacion,
            password=hashed_password  # Guardar la contraseña encriptada
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario

    # 🔹 Actualizar un usuario
    def actualizar_usuario(db: Session, usuario_id: int, usuario_update: UsuarioUpdate):
        usuario = obtener_usuario(db, usuario_id)

        if usuario_update.password:
            usuario_update.password = pwd_context.hash(usuario_update.password)  # 🔒 Encriptar nueva contraseña

        for key, value in usuario_update.dict(exclude_unset=True).items():
            setattr(usuario, key, value)

        db.commit()
        db.refresh(usuario)
        return usuario

    # 🔹 Eliminar un usuario
    def eliminar_usuario(db: Session, usuario_id: int):
        usuario = obtener_usuario(db, usuario_id)
        db.delete(usuario)
        db.commit()
        return {"message": "Usuario eliminado"}

    OTHERS SCHEMAS

    # ==============================
    # 🔹 USUARIO SCHEMAS
    # ==============================

    class UsuarioBase(BaseModel):
        nombre: str
        apellido: Optional[str] = None
        email: EmailStr
        rol: str
        fecha_creacion: date

        @validator("fecha_creacion", pre=True, always=True)
        def convert_fecha_creacion(cls, v):
            if isinstance(v, datetime):
                return v.date()  # ✅ Convertir datetime a date
            return v
        class Config:
            from_attributes = True  # ✅ Reemplazo de orm_mode en Pydantic v2

    class UsuarioCreate(UsuarioBase):
        password: str  # ✅ Agregado campo password para creación

    class UsuarioUpdate(BaseModel):
        nombre: Optional[str] = None
        apellido: Optional[str] = None
        email: Optional[str] = None
        password: Optional[str] = None
        rol: Optional[str] = None
        fecha_creacion: Optional[date] = None

    class UsuarioRead(UsuarioBase):
        id: int
        operaciones: List[ForwardRef("OperacionRead")] = []  # ✅ Evita referencias circulares

        class Config:
            from_attributes = True

    # ==============================
    # 🔹 INSUMO SCHEMAS
    # ==============================
    class InsumoBase(BaseModel):
        nombre: str
        unidad: str

    class InsumoCreate(InsumoBase):
        pass

    class InsumoUpdate(BaseModel):
        nombre: Optional[str] = None
        unidad: Optional[str] = None

    class Insumo(InsumoBase):
        id: int

        class Config:
            from_attributes = True

    # ==============================
    # 🔹 DETALLE INSUMO CONSUMIDO SCHEMAS
    # ==============================
    class DetalleInsumoConsumidoBase(BaseModel):
        operacion_id: int
        insumo_id: int
        cantidad: float

    class DetalleInsumoConsumidoCreate(DetalleInsumoConsumidoBase):
        pass

    class DetalleInsumoConsumidoUpdate(BaseModel):
        operacion_id: Optional[int] = None
        insumo_id: Optional[int] = None
        cantidad: Optional[float] = None

    class DetalleInsumoConsumido(DetalleInsumoConsumidoBase):
        id: int
        operacion: "OperacionRead"  # ✅ Usar ForwardRef para evitar referencia circular
        insumo: "Insumo"

        class Config:
            from_attributes = True

    # ==============================
    # 🔹 SOLUCIONAR REFERENCIAS CIRCULARES
    # ==============================
    UsuarioRead.model_rebuild()  # ✅ Corrige referencias circulares
    OperacionRead.model_rebuild()
    DetalleInsumoConsumido.model_rebuild()
'''}