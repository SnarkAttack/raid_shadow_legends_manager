from sqlalchemy.orm import Session
from functools import wraps

def session_managed(engine):
    def session_managed_wrap(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            existing_session = True
            session = kwargs.get('session')
            if session is None:
                session = Session(engine)
                existing_session = False
            else:
                del kwargs['session']
            res = func(session, *args, **kwargs)
            session.commit()
            if not existing_session:
                session.close()
            return res
        return wrap
    return session_managed_wrap

def cm_session_managed(engine):
    """

    Utility wrapper to allowed classmethod functions to be wrapped in a function that
    will generate and then clean up a session for an function that:
        1) Queries the database
        2) DOES NOT return an ORM object

    If an ORM object is going to be returned, the session must be passed in as a deliberately
    created object elsewhere so the ORM object is still available when the function completes

    All functions wrapped by this method must also be wrapped in @classmethod and have their 
    first two arguments be cls and session, e.g.

        def some_func(cls, session, *args, **kwargs)

    Parameters
    ----------
    engine: sqlalchemy.engine.Engine: the engine to use for database connectivity
    
    """
    def cm_session_managed_wrap(func):
        @wraps(func)
        def cm_wrap(cls, *args, **kwargs):
            session = Session(engine)
            res = func(cls, session, *args, **kwargs)
            session.commit()
            session.close()
            return res
        return cm_wrap
    return cm_session_managed_wrap

def s_session_managed(engine):
    def s_session_managed_wrap(func):
        @wraps(func)
        def s_wrap(cls, *args, **kwargs):
            session = Session(engine)
            res = func(cls, session, *args, **kwargs)
            session.commit()
            session.close()
            return res
        return s_wrap
    return s_session_managed_wrap



