from . import Constant as ctx
from ..utility import Processor
from ..database import *
from ..connection import *

class Core:

	def __init__(self) -> None:

		# Setup Database
		self.settings = Settings(ctx.DATABASE_FOLDER.joinpath('settings.json'))
		self.tags = Tags(ctx.DATABASE_FOLDER.joinpath('tags.json'))
		self.table = Tags(ctx.DATABASE_FOLDER.joinpath('tags.json'))

		# Setup connection
		self.sonarr = Sonarr(ctx.SONARR_URL, ctx.API_KEY)
		self.processor = Processor(self)

	def job(self):
		