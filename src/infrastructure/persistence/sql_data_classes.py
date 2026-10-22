from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from sqlalchemy import ForeignKey, String, Text, Integer, Boolean, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "person"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    email: Mapped[Optional[str]] = mapped_column(String)
    name: Mapped[Optional[str]] = mapped_column(String)

    # Relationships
    projects_led: Mapped[List["Project"]] = relationship("Project", back_populates="lead", foreign_keys="[Project.lead_id]")
    issues_assigned: Mapped[List["Issue"]] = relationship("Issue", back_populates="assignee", foreign_keys="[Issue.assignee_id]")
    issues_created: Mapped[List["Issue"]] = relationship("Issue", back_populates="creator", foreign_keys="[Issue.creator_id]")
    issues_reported: Mapped[List["Issue"]] = relationship("Issue", back_populates="reporter", foreign_keys="[Issue.reporter_id]")
    attachments: Mapped[List["Attachment"]] = relationship("Attachment", back_populates="author", foreign_keys="[Attachment.author_id]")
    comments_authored: Mapped[List["Comment"]] = relationship("Comment", back_populates="author", foreign_keys="[Comment.author_id]")
    comments_updated: Mapped[List["Comment"]] = relationship("Comment", back_populates="updater", foreign_keys="[Comment.updater_id]")
    changes_made: Mapped[List["Change"]] = relationship("Change", back_populates="author", foreign_keys="[Change.author_id]")


class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)
    archived: Mapped[bool] = mapped_column(Boolean)
    assignee_type: Mapped[Optional[str]] = mapped_column(String)
    type_key: Mapped[Optional[str]] = mapped_column(String)
    lead_id: Mapped[Optional[str]] = mapped_column(ForeignKey("person.id"))

    # Relationships
    lead: Mapped[Optional["Person"]] = relationship("Person", back_populates="projects_led")
    issues: Mapped[List["Issue"]] = relationship("Issue", back_populates="project")
    workflows: Mapped[List["Workflow"]] = relationship("Workflow", back_populates="project")


class IssueType(Base):
    __tablename__ = "issue_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[str] = mapped_column(String)

    issues: Mapped[List["Issue"]] = relationship("Issue", back_populates="issue_type")


class Priority(Base):
    __tablename__ = "priority"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[str] = mapped_column(String)

    issues: Mapped[List["Issue"]] = relationship("Issue", back_populates="priority")


class Resolution(Base):
    __tablename__ = "resolution"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    value: Mapped[str] = mapped_column(String)

    issues: Mapped[List["Issue"]] = relationship("Issue", back_populates="resolution")


class Status(Base):
    __tablename__ = "status"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)

    issues: Mapped[List["Issue"]] = relationship("Issue", back_populates="status")
    workflows_from: Mapped[List["Workflow"]] = relationship("Workflow", foreign_keys="[Workflow.from_status_id]")
    workflows_to: Mapped[List["Workflow"]] = relationship("Workflow", foreign_keys="[Workflow.to_status_id]")


class Issue(Base):
    __tablename__ = "issue"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String, unique=True)
    assignee_id: Mapped[Optional[str]] = mapped_column(ForeignKey("person.id"))
    creator_id: Mapped[str] = mapped_column(ForeignKey("person.id"))
    reporter_id: Mapped[str] = mapped_column(ForeignKey("person.id"))
    issue_type_id: Mapped[int] = mapped_column(ForeignKey("issue_type.id"))
    priority_id: Mapped[int] = mapped_column(ForeignKey("priority.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))
    resolution_id: Mapped[Optional[int]] = mapped_column(ForeignKey("resolution.id"))
    status_id: Mapped[int] = mapped_column(ForeignKey("status.id"))
    created_date: Mapped[datetime] = mapped_column(DateTime)
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    resolution_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    summary: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)

    # Relationships
    assignee: Mapped[Optional["Person"]] = relationship("Person", back_populates="issues_assigned", foreign_keys=[assignee_id])
    creator: Mapped["Person"] = relationship("Person", back_populates="issues_created", foreign_keys=[creator_id])
    reporter: Mapped["Person"] = relationship("Person", back_populates="issues_reported", foreign_keys=[reporter_id])
    issue_type: Mapped["IssueType"] = relationship("IssueType", back_populates="issues")
    priority: Mapped["Priority"] = relationship("Priority", back_populates="issues")
    project: Mapped["Project"] = relationship("Project", back_populates="issues")
    resolution: Mapped[Optional["Resolution"]] = relationship("Resolution", back_populates="issues")
    status: Mapped["Status"] = relationship("Status", back_populates="issues")

    issuelinks_inward: Mapped[List["IssueLink"]] = relationship("IssueLink", backref="inward_issue", foreign_keys="[IssueLink.inward_issue_id]")
    issuelinks_outward: Mapped[List["IssueLink"]] = relationship("IssueLink", backref="outward_issue", foreign_keys="[IssueLink.outward_issue_id]")
    labels: Mapped[List["Label"]] = relationship("Label", back_populates="issue")
    attachments: Mapped[List["Attachment"]] = relationship("Attachment", back_populates="issue")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="issue")
    changes: Mapped[List["Change"]] = relationship("Change", back_populates="issue")


class IssueLinkType(Base):
    __tablename__ = "issuelink_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    inward_name: Mapped[str] = mapped_column(String)
    outward_name: Mapped[str] = mapped_column(String)

    issuelinks: Mapped[List["IssueLink"]] = relationship("IssueLink", back_populates="link_type")


class IssueLink(Base):
    __tablename__ = "issuelink"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("issuelink_type.id"))
    inward_issue_id: Mapped[int] = mapped_column(ForeignKey("issue.id"))
    outward_issue_id: Mapped[int] = mapped_column(ForeignKey("issue.id"))

    # Relationships
    link_type: Mapped["IssueLinkType"] = relationship("IssueLinkType", back_populates="issuelinks")
    inward_issue: Mapped["Issue"] = relationship("Issue", foreign_keys=[inward_issue_id], backref="inward_link_to")
    outward_issue: Mapped["Issue"] = relationship("Issue", foreign_keys=[outward_issue_id], backref="outward_link_to")


class Label(Base):
    __tablename__ = "label"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey("issue.id"))
    value: Mapped[str] = mapped_column(String)

    issue: Mapped["Issue"] = relationship("Issue", back_populates="labels")


class Attachment(Base):
    __tablename__ = "attachment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey("issue.id"))
    author_id: Mapped[str] = mapped_column(ForeignKey("person.id"))
    created_date: Mapped[datetime] = mapped_column(DateTime)
    file_name: Mapped[str] = mapped_column(String)
    file_size: Mapped[int] = mapped_column(Integer)
    local_path: Mapped[str] = mapped_column(String)
    mime_type: Mapped[str] = mapped_column(String)

    issue: Mapped["Issue"] = relationship("Issue", back_populates="attachments")
    author: Mapped["Person"] = relationship("Person", back_populates="attachments")


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey("issue.id"))
    author_id: Mapped[str] = mapped_column(ForeignKey("person.id"))
    updater_id: Mapped[str] = mapped_column(ForeignKey("person.id"))
    created_date: Mapped[datetime] = mapped_column(DateTime)
    updated_date: Mapped[datetime] = mapped_column(DateTime)
    body: Mapped[str] = mapped_column(Text)

    issue: Mapped["Issue"] = relationship("Issue", back_populates="comments")
    author: Mapped["Person"] = relationship("Person", back_populates="comments_authored", foreign_keys=[author_id])
    updater: Mapped["Person"] = relationship("Person", back_populates="comments_updated", foreign_keys=[updater_id])


class Change(Base):
    __tablename__ = "change"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey("issue.id"))
    author_id: Mapped[str] = mapped_column(ForeignKey("person.id"))
    created_date: Mapped[datetime] = mapped_column(DateTime)
    field: Mapped[str] = mapped_column(String)
    field_type: Mapped[str] = mapped_column(String)
    from_value: Mapped[str] = mapped_column(String)
    to_value: Mapped[str] = mapped_column(String)

    issue: Mapped["Issue"] = relationship("Issue", back_populates="changes")
    author: Mapped["Person"] = relationship("Person", back_populates="changes_made", foreign_keys=[author_id])


class Workflow(Base):
    __tablename__ = "workflow"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))
    from_status_id: Mapped[int] = mapped_column(ForeignKey("status.id"))
    to_status_id: Mapped[int] = mapped_column(ForeignKey("status.id"))

    project: Mapped["Project"] = relationship("Project", back_populates="workflows")
    from_status: Mapped["Status"] = relationship("Status", foreign_keys=[from_status_id])
    to_status: Mapped["Status"] = relationship("Status", foreign_keys=[to_status_id])
