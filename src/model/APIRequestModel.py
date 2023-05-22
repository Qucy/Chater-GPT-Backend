from pydantic import BaseModel, Field

class Translation(BaseModel):
    """
    Translation model for API request
    """

    chat_id: str

    target_language: str | None = Field(
        default = 'English', title="Taget translation language"
    )

    style : str | None = Field(
        default = 'formal', title="Style of translation", max_length=20
    )
    
    content: str | None = Field(
        default = 'Hello world!', title="Content to be translated", max_length=500
    )


class GrammerCorrection(BaseModel):
    """
    Grammer correction model for API request
    """

    chat_id: str

    content: str | None = Field(
        default = 'Hello world!', title="Content to be corrected", max_length=500
    )


class TLDRSummarization(BaseModel):
    """
    Text summarization model for API request
    """
    chat_id: str

    target_language: str | None = Field(
        default = 'English', title="Taget summarization language"
    )

    content_length : int | None = Field(
        default = 100, title="Length of summary"
    )

    content : str | None = Field(
        default = 'Hello world!', title="Content to be summarized", max_length=3000
    )


class RestaurantReviewCreator(BaseModel):
    """
    Restaurant review creator model for API request
    """
    chat_id: str

    target_language: str | None = Field(
        default = 'English', title="Taget review language"
    )

    content_length : int | None = Field(
        default = 100, title="Length of review"
    )

    content_category : str | None = Field(
        default = 'Positive', title="Category of review - positive or negative", max_length=20
    )

    content : str | None = Field(
        default = 'Hello world!', title="Content to be reviewed", max_length=500
    )

class ChatContentModel(BaseModel):

    role: str | None = Field(
        default = 'user', title="Role of the chat content", max_length=20
    )

    content: str | None = Field(
        default = 'Hello, how are you today!', title="Content to be send to backend", max_length=2000
    )

class FriendChatModel(BaseModel):
    """
    Freind chat model for API request
    """
    chat_id: str

    contents : list[ChatContentModel] | None = Field(
        default = [], title="List of chat contents"
    )